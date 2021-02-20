from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch
import torch.nn as nn
from enum import Enum

import torch.nn.functional as F
from torch.distributions import Categorical
import csv, random, re, os, math

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Seq2SeqTransformer(nn.Module):
    def __init__(self, input_size, hidden_size, target_vocab, num_heads, num_encoder_layers, num_decoder_layers, forward_expansion, input_vocab=None, dropout=0.1, max_len=50, learned_pos_embeddings=False, device=torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        '''A Seq2Seq Transformer which embeds inputs and outputs distributions over the output vocab\n
        Init Inputs:
            input_size (int): The size of embeddings in the network
            hidden_size (int): The size of hidden vectors in the network
            target_vocab (vocab): The target vocab
            num_heads (int): The number of heads in both the encoder and decoder
            num_encoder_layers (int): The number of layers in the transformer encoder
            num_decoder_layers (int): The number of layers in the transformer decoder
            forward_expansion (int): The factor of expansion in the elementwise feedforward layer
            input_vocab (vocab) [Default: None]: The input vocab, if none, then inputs are already expected as vectors
            dropout (float) [Default: 0.1]: The amount of dropout
            max_len (int) [Default: 50]: The max target length used when a target is not provided
            learned_pos_embeddings (bool) [Default: False]: To use learned positional embeddings or fixed ones
            device (torch.device): The device that the network will run on
        Inputs:
            src (Tensor): The input sequence of shape (src length, batch size)
            trg (Tensor) [default=None]: The target sequence of shape (trg length, batch size)
        Returns:
            output (Tensor): The return sequence of shape (target length, batch size, target tokens)'''
        super().__init__()
        assert hidden_size % num_heads == 0, "hidden_size must be divisible by num_heads"
        self.hyperparameters = locals()
        self.device = device
        self.input_vocab = input_vocab
        self.target_vocab = target_vocab
        self.max_len = max_len
        self.input_size = input_size
        if input_vocab is not None: self.src_embedding = nn.Embedding(input_vocab.num_words, input_size)
        self.src_positional_embedding = nn.Embedding(max_len, input_size) if learned_pos_embeddings else self.generate_pos_embeddings
        self.trg_embedding = nn.Embedding(target_vocab.num_words, input_size)
        self.trg_positional_embedding = nn.Embedding(max_len, input_size) if learned_pos_embeddings else self.generate_pos_embeddings
        self.transformer = nn.Transformer(d_model=hidden_size, dim_feedforward=hidden_size * forward_expansion, nhead=num_heads, num_encoder_layers=num_encoder_layers, num_decoder_layers=num_decoder_layers, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.fc_out = nn.Linear(hidden_size, target_vocab.num_words)
        self.convert_input = nn.Linear(input_size, hidden_size) if input_size != hidden_size else None

    def generate_pos_embeddings(self, seq): # Generate statc positional embeddings of shape (seq len, batch size, embed size)
        '''seq: (seq len, 1) or (seq len)'''
        pe = torch.zeros(seq.shape[0], self.input_size, device=self.device)
        position = torch.arange(0, seq.shape[0], dtype=torch.float, device=self.device).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, self.input_size, 2).float().to(device) * (-math.log(10000.0) / self.input_size))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        return pe[:, :]

    def forward(self, src, trg=None):
        '''src: (seq len, batch size)\n
        trg: (seq len, batch size) or None'''
        if len(src.shape) == 2: src_len, batch_size = src.shape
        else: src_len, batch_size, input_dims = src.shape
        assert src_len < self.max_len, "Input was too large! The input must be less than " + str(self.max_len) + " tokens!"

        # Handle target given/autoregressive
        if trg is None:
            autoregressive = True
            trg = torch.full((1, batch_size), fill_value=self.target_vocab.SOS_token, dtype=torch.long, device=self.device)
        else:
            autoregressive = False
            if trg[0][0].item() != self.target_vocab.SOS_token: # Ensure there is an SOS token at the start of the trg, add if there isn't
                trg = torch.cat((torch.full((1, batch_size), fill_value=self.target_vocab.SOS_token, dtype=torch.long, device=self.device), trg), dim=0)
            if any(trg[-1, :] == self.target_vocab.EOS_token): # Ensure there is no EOS token in the target
                # Make lists without EOS tokens
                temp_trg = [row[(row != self.target_vocab.EOS_token)] for row in trg.transpose(0, 1)]
                trg = torch.stack(temp_trg).transpose(0, 1)
        
        # Embed src
        src_positions = torch.arange(0, src_len, device=self.device).unsqueeze(1).expand(src_len, batch_size)
        if len(src.shape) == 2:
            src_pad_mask = (src == self.input_vocab.PAD_token).transpose(0, 1)
            src_embed = self.src_embedding(src) * math.sqrt(self.input_size) + self.src_positional_embedding(src_positions)
            #src_embed = self.src_embedding(src)
        else:
            src_pad_mask = None
            src_embed = src * math.sqrt(self.input_size) + self.src_positional_embedding(src_positions)
            #src_embed = src
        # Convert src input_dims to hidden_dims if nessacary
        if self.convert_input is not None: src_embed = self.convert_input(src_embed)

        for i in range(self.max_len if autoregressive else 1):
            # Get target pad mask
            trg_pad_mask = (trg == self.target_vocab.PAD_token).transpose(0, 1)

            # Embed target
            trg_positions = torch.arange(0, trg.shape[0], device=self.device).unsqueeze(1).expand(trg.shape[0], batch_size)
            trg_embed = self.trg_embedding(trg) * math.sqrt(self.input_size) + self.trg_positional_embedding(trg_positions)
            #trg_embed = self.trg_embedding(trg)
            if self.convert_input is not None: trg_embed = self.convert_input(trg_embed)

            # Get target subsequent mask
            trg_subsequent_mask = self.transformer.generate_square_subsequent_mask(trg.shape[0]).to(self.device)

            # Feed through model
            out = self.transformer(src=src_embed, tgt=trg_embed, src_key_padding_mask=src_pad_mask, tgt_key_padding_mask=trg_pad_mask, tgt_mask=trg_subsequent_mask)
            
            if out.isnan().any(): 
                print("Src: " + str(src_embed.isnan().any()))
                print("Trg: " + str(trg_embed.isnan().any()))
                print("Out: " + str(out.isnan().any()))
            
            out = self.fc_out(out)
            # out shape: (trg_len, batch size, target_num_words)

            if autoregressive:
                # Get the soft embedding
                dist = Categorical(logits=out[-1])
                trg = torch.cat((trg, dist.sample().unsqueeze(0)), dim=0)
                if all([any(trg[:, x] == self.target_vocab.EOS_token) for x in range(batch_size)]): # EOS was outputted in all batches
                    break

        # out shape: (trg_len, batch size, target_num_words)
        return F.softmax(out, dim=-1)

class TransformerEncoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_heads, num_layers, forward_expansion, input_vocab=None, dropout=0.1, max_len=50, learned_pos_embeddings=False, device=torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        '''A Transformer emcoder which encodes inputs into encoded vectors\n
        Init Inputs:
            input_size (int): The size of embeddings in the network
            hidden_size (int): The size of hidden vectors in the network
            num_heads (int): The number of heads in both the encoder and decoder
            num_layers (int): The number of layers in the transformer encoder
            forward_expansion (int): The factor of expansion in the elementwise feedforward layer
            input_vocab (vocab) [Default: None]: The input vocab, if none, then inputs are already expected as vectors
            dropout (float) [Default: 0.1]: The amount of dropout
            max_len (int) [Default: 50]: The max target length used when a target is not provided
            learned_pos_embeddings (bool) [Default: False]: To use learned positional embeddings or fixed ones
            device (torch.device): The device that the network will run on
        Inputs:
            src (Tensor): The input sequence of shape (src length, batch size)
        Returns:
            output (Tensor): The return sequence of shape (target length, batch size, target tokens)'''
        super().__init__()
        self.hyperparameters = locals()
        self.device = device
        self.input_vocab = input_vocab
        self.max_len = max_len
        self.input_size = input_size
        if input_vocab is not None: self.src_embedding = nn.Embedding(input_vocab.num_words, input_size)
        self.src_positional_embedding = nn.Embedding(max_len, input_size) if learned_pos_embeddings else self.generate_pos_embeddings
        self.transformer_encoder = nn.TransformerEncoder(nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads, dim_feedforward=hidden_size * forward_expansion, dropout=dropout), num_layers=num_layers)
        self.dropout = nn.Dropout(dropout)
        self.convert_input = nn.Linear(input_size, hidden_size) if input_size != hidden_size else None

    def generate_pos_embeddings(self, seq): # Generate statc positional embeddings of shape (seq len, batch size, embed size)
        '''seq: (seq len, 1) or (seq len)'''
        pe = torch.zeros(seq.shape[0], self.input_size, device=self.device)
        position = torch.arange(0, seq.shape[0], dtype=torch.float, device=self.device).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, self.input_size, 2).float().to(self.device) * (-math.log(10000.0) / self.input_size))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        return pe[:, :]

    def forward(self, src):
        '''src: (seq len, batch size) or (seq len, batch size, embed dims)'''
        if self.input_vocab is not None and len(src.shape) == 2: src_len, batch_size = src.shape
        else: src_len, batch_size, input_dims = src.shape
        assert src_len < self.max_len, "Input was too large! The input must be less than " + str(self.max_len) + " tokens!"

        # Embed src
        src_positions = torch.arange(0, src_len, device=self.device).unsqueeze(1).expand(src_len, batch_size)
        if self.input_vocab is not None and len(src.shape) == 2:
            src_pad_mask = (src == self.input_vocab.PAD_token).transpose(0, 1)
            src_embed = self.src_embedding(src) + self.src_positional_embedding(src_positions)
        else:
            src_pad_mask = None
            src_embed = src + self.src_positional_embedding(src_positions)
        # Convert src input_dims to hidden_dims if nessacary
        if self.convert_input is not None: src_embed = self.convert_input(src_embed)
        out = self.transformer_encoder(src=src_embed, src_key_padding_mask=(src == self.input_vocab.PAD_token).transpose(0, 1) if self.input_vocab is not None and len(src.shape) == 2 else None)
        return out

class TransformerAggregator(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_heads, num_layers, forward_expansion, input_vocab=None, dropout=0.1, max_len=50, learned_pos_embeddings=False, device=torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        '''A Transformer aggregator which encodes inputs into a single aggregated vector\n
        Init Inputs:
            input_size (int): The size of embeddings in the network
            hidden_size (int): The size of hidden vectors in the network
            output_size (int): The size of the aggregated vector
            num_heads (int): The number of heads in both the encoder and decoder
            num_layers (int): The number of layers in the transformer encoder
            forward_expansion (int): The factor of expansion in the elementwise feedforward layer
            input_vocab (vocab) [Default: None]: The input vocab, if none, then inputs are already expected as vectors
            dropout (float) [Default: 0.1]: The amount of dropout
            max_len (int) [Default: 50]: The max target length used when a target is not provided
            learned_pos_embeddings (bool) [Default: False]: To use learned positional embeddings or fixed ones
            device (torch.device): The device that the network will run on
        Inputs:
            src (Tensor): The input sequence of shape (src length, batch size) or (src length, batch size, embed size)
        Returns:
            output (Tensor): The return sequence of shape (target length, batch size, target tokens)'''
        super().__init__()
        self.encoder = TransformerEncoder(input_size=input_size, hidden_size=hidden_size, num_heads=num_heads, num_layers=num_layers, forward_expansion=forward_expansion, input_vocab=input_vocab, dropout=dropout, max_len=max_len, learned_pos_embeddings=learned_pos_embeddings, device=device)
        self.out = nn.Linear(hidden_size, output_size)
        self.aggregate_input_vector = nn.Parameter(torch.randn(input_size, requires_grad=True), requires_grad=True) # Learned input vector for the aggregating position, like CLS for BERT

    def forward(self, input_seq):
        '''src (Tensor): The input sequence of shape (src length, batch size) or (src length, batch size, embed size)\n
        The input sequence should NOT have an aggregating vector (CLS) already on it.'''
        # Append aggregate vector to the beginning
        input_seq = torch.cat((self.aggregate_input_vector.unsqueeze(0).unsqueeze(0).repeat(1, input_seq.shape[1], 1), (self.encoder.src_embedding(input_seq) if len(input_seq.shape) == 2 else input_seq)), dim=0)
        output = self.encoder(input_seq)
        return self.out(output[0])

# Raw transformer layers
class Embeddings(nn.Module):
    """
    Implements embeddings of the words and adds their positional encodings. 
    """
    def __init__(self, vocab_size, d_model, max_len=50):
        super(Embeddings, self).__init__()
        self.d_model = d_model
        self.dropout = nn.Dropout(0.1)
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pe = self.create_positinal_encoding(max_len, self.d_model)
        self.dropout = nn.Dropout(0.1)
        
    def create_positinal_encoding(self, max_len, d_model):
        pe = torch.zeros(max_len, d_model).to(device)
        for pos in range(max_len):   # for each position of the word
            for i in range(0, d_model, 2):   # for each dimension of the each position
                pe[pos, i] = math.sin(pos / (10000 ** ((2 * i)/d_model)))
                pe[pos, i + 1] = math.cos(pos / (10000 ** ((2 * (i + 1))/d_model)))
        pe = pe.unsqueeze(0)   # include the batch size
        return pe
        
    def forward(self, encoded_words):
        embedding = self.embed(encoded_words) * math.sqrt(self.d_model)
        embedding += self.pe[:, :embedding.size(1)]   # pe will automatically be expanded with the same batch size as encoded_words
        embedding = self.dropout(embedding)
        return embedding



class MultiHeadAttention(nn.Module):
    def __init__(self, heads, d_model):
        
        super(MultiHeadAttention, self).__init__()
        assert d_model % heads == 0
        self.d_k = d_model // heads
        self.heads = heads
        self.dropout = nn.Dropout(0.1)
        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)
        self.concat = nn.Linear(d_model, d_model)
        
    def forward(self, query, key, value, mask):
        """
        query, key, value of shape: (batch_size, max_len, 512)
        mask of shape: (batch_size, 1, 1, max_words)
        """
        # (batch_size, max_len, 512)
        query = self.query(query)
        key = self.key(key)        
        value = self.value(value)   
        
        # (batch_size, max_len, 512) --> (batch_size, max_len, h, d_k) --> (batch_size, h, max_len, d_k)
        query = query.view(query.shape[0], -1, self.heads, self.d_k).permute(0, 2, 1, 3)   
        key = key.view(key.shape[0], -1, self.heads, self.d_k).permute(0, 2, 1, 3)  
        value = value.view(value.shape[0], -1, self.heads, self.d_k).permute(0, 2, 1, 3)  
        
        # (batch_size, h, max_len, d_k) matmul (batch_size, h, d_k, max_len) --> (batch_size, h, max_len, max_len)
        scores = torch.matmul(query, key.permute(0,1,3,2)) / math.sqrt(query.size(-1))
        scores = scores.masked_fill(mask == 0, -1e9)    # (batch_size, h, max_len, max_len)
        weights = F.softmax(scores, dim=-1)           # (batch_size, h, max_len, max_len)
        weights = self.dropout(weights)
        # (batch_size, h, max_len, max_len) matmul (batch_size, h, max_len, d_k) --> (batch_size, h, max_len, d_k)
        context = torch.matmul(weights, value)
        # (batch_size, h, max_len, d_k) --> (batch_size, max_len, h, d_k) --> (batch_size, max_len, h * d_k)
        context = context.permute(0,2,1,3).contiguous().view(context.shape[0], -1, self.heads * self.d_k)
        # (batch_size, max_len, h * d_k)
        interacted = self.concat(context)
        return interacted 



class FeedForward(nn.Module):
    def __init__(self, d_model, middle_dim=2048):
        super(FeedForward, self).__init__()
        
        self.fc1 = nn.Linear(d_model, middle_dim)
        self.fc2 = nn.Linear(middle_dim, d_model)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        out = F.relu(self.fc1(x))
        out = self.fc2(self.dropout(out))
        return out


class EncoderLayer(nn.Module):
    def __init__(self, d_model, heads):
        super(EncoderLayer, self).__init__()
        self.layernorm = nn.LayerNorm(d_model)
        self.self_multihead = MultiHeadAttention(heads, d_model)
        self.feed_forward = FeedForward(d_model)
        self.dropout = nn.Dropout(0.1)

    def forward(self, embeddings, mask):
        interacted = self.dropout(self.self_multihead(embeddings, embeddings, embeddings, mask))
        interacted = self.layernorm(interacted + embeddings)
        feed_forward_out = self.dropout(self.feed_forward(interacted))
        encoded = self.layernorm(feed_forward_out + interacted)
        return encoded


class DecoderLayer(nn.Module):
    def __init__(self, d_model, heads):
        super(DecoderLayer, self).__init__()
        self.layernorm = nn.LayerNorm(d_model)
        self.self_multihead = MultiHeadAttention(heads, d_model)
        self.src_multihead = MultiHeadAttention(heads, d_model)
        self.feed_forward = FeedForward(d_model)
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, embeddings, encoded, src_mask, target_mask):
        query = self.dropout(self.self_multihead(embeddings, embeddings, embeddings, target_mask))
        query = self.layernorm(query + embeddings)
        interacted = self.dropout(self.src_multihead(query, encoded, encoded, src_mask))
        interacted = self.layernorm(interacted + query)
        feed_forward_out = self.dropout(self.feed_forward(interacted))
        decoded = self.layernorm(feed_forward_out + interacted)
        return decoded


class Transformer(nn.Module):
    def __init__(self, d_model, heads, num_layers, local_vocab):
        super(Transformer, self).__init__()
        
        self.d_model = d_model
        self.vocab_size = local_vocab.num_words
        self.local_vocab = local_vocab
        self.embed = Embeddings(self.vocab_size, d_model)
        self.encoder = nn.ModuleList([EncoderLayer(d_model, heads) for _ in range(num_layers)])
        self.decoder = nn.ModuleList([DecoderLayer(d_model, heads) for _ in range(num_layers)])
        self.logit = nn.Linear(d_model, self.vocab_size)
        
    def encode(self, src_words, src_mask):
        src_embeddings = self.embed(src_words)
        for layer in self.encoder:
            src_embeddings = layer(src_embeddings, src_mask)
        return src_embeddings
    
    def decode(self, target_words, target_mask, src_embeddings, src_mask):
        tgt_embeddings = self.embed(target_words)
        for layer in self.decoder:
            tgt_embeddings = layer(tgt_embeddings, src_embeddings, src_mask, target_mask)
        return tgt_embeddings
        
    def forward(self, src_words, target_words):
        src_mask = (src_words != self.local_vocab.PAD_token)
        trg_mask = (target_words != self.local_vocab.PAD_token)
        encoded = self.encode(src_words, src_mask)
        decoded = self.decode(target_words, trg_mask, encoded, src_mask)
        out = F.log_softmax(self.logit(decoded), dim=2)
        return out