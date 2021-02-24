import re
import pymorphy2
import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize

class Separatrice:
  def __init__(self):
    self.alphabets= "([А-Яа-я])"
    self.acronyms = "([А-Яа-я][.][А-Яа-я][.](?:[А-Яа-я][.])?)"
    self.prefixes = "(Mr|Mrs|Ms|акад|чл.-кор|канд|доц|проф|ст|мл|ст. науч|мл. науч|рук|тыс|млрд|млн|кг|км|м|мин|сек|ч|мл|нед|мес|см|сут|проц)[.]"
    self.starters = "(Mr|Mrs|Ms|Dr)"
    self.websites = "[.](com|net|org|io|gov|ru|xyz|ру)"
    self.suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    self.conjs = '(, что|чтобы|, когда| несмотря на то что| вопреки|, а также| либо| но| зато|, а| тогда|, а то| так что| чтоб| затем| дабы| коль скоро| если бы| если б| коль скоро| тогда как| как только| подобно тому как| будто бы)'
    self.introductory = '(вот где где,|не-а,|и ещё|во-первых|во-вторых|конечно|несомненно|без всякого сомнения|очевидно|безусловно|разумеется|само собой разумеется|бесспорно|действительно,|наверное|возможно|верно|вероятно|по всей вероятности|может быть|быть может|должно быть|кажется|казалось бы|видимо|по-видимому|пожалуйста|в самом деле|подлинно|правда|не правда ли|в сущности|по существу|по сути|надо полагать|к счастью|к несчастью|по счастью|по несчастью|к радости|к огорчению|к прискорбию|к досаде|к сожалению|к удивлению|к изумлению|к ужасу|к стыду|говорят|сообщают|передают|по словам|по сообщению|по сведениям|по мнению|по-моему|по-твоему|по-нашему|по-вашему|на мой взгляд|по слухам|по преданию|помнится|слышно|дескать|говорят|сообщают|передают|по словам|по сообщению|по сведениям|по мнению|по-моему|по-твоему|по-нашему|по-вашему|на мой взгляд|по слухам|по преданию|помнится|слышно|дескать|словом|одним словом|иными словами|другими словами|иначе говоря|коротко говоря|попросту сказать|мягко выражаясь|если можно так сказать|если можно так выразиться|с позволения сказать|лучше сказать|так сказать|что называется и другие; слова собственно|вообще|вернее|точнее|скорее |видишь ли|видите ли|понимаешь ли|понимаете ли|знаешь ли|знаете ли|пойми|поймите|поверьте|послушайте|согласитесь|вообразите|представьте себе|извините|простите|веришь ли|верите ли|пожалуйста|спасибо|привет|пасиб|прив|здравствуйте|доброго дня|доброго вечера)'
    self.morph = pymorphy2.MorphAnalyzer()
  
  def into_sents(self,text):
    flag = False
    if text[-1] != '.' and text[-1] != '!' and text[-1] != '?':
      text += '.'
      flag = True
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(' '+self.prefixes,"\\1<prd>",text)
    text = re.sub(self.websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + self.alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(self.acronyms+" "+self.starters,"\\1<stop> \\2",text)
    text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]" + self.alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+self.suffixes+"[.] "+self.starters," \\1<stop> \\2",text)
    text = re.sub(" "+self.suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + self.alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(". ",".<stop>")
    text = text.replace("? ","?<stop>")
    text = text.replace("! ","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    if (flag == True):
      sentences[-1] = sentences[-1][:-1]
    sentences = [s.strip() for s in sentences if s not in ["!","?",'.']]
    return sentences
  
  def introductory_phrase(self, sent):
    tokens = word_tokenize(sent)
    comma = False
    i = 0
    tag = self.morph.parse(tokens[i])[0].tag
    while (('NOUN' in tag or 'ADJS' in tag or 'ADJF' in tag or 'ADJS' in tag or 'NPRO' in tag) or tokens[i] == ','):
        if (tokens[i] == ','):
          comma = True
          break
        if i < len(tokens)-1:
          i += 1
          tag = self.morph.parse(tokens[i])[0].tag
        else:
          break

    if comma:    
      return ' '.join(tokens[:i])
    else:
      return '' 
  
  # check whether or not text contains predicate
  def _pred_in(self,text,subj_required=False):
    '''
    params
    ---
    text : str
    return
    ---
    bool
    '''
    tokenized = text.strip(' ').split(' ')
    noun = False
    pron = False
    adj = False
    prt = False
    verb = False
    for word in tokenized:
      word = word.strip('.')
      word = word.strip('!')
      word = word.strip('?')
      word = word.strip(',')
      if ('VERB' in self.morph.parse(word)[0].tag or 'INFN' in self.morph.parse(word)[0].tag or 'PRED' in self.morph.parse(word)[0].tag
            or 'нет' == word or 'здесь' == word or 'тут' == word or '-' == word or '—' == word):
          return True
      if ('это' == word):
        pron = True
      elif ('ADJF' in self.morph.parse(word)[0].tag or 'ADJS' in self.morph.parse(word)[0].tag):
        adj = True
      elif (len(self.morph.parse(word)) > 1):
        if ('ADJF' in self.morph.parse(word)[1].tag or 'ADJS' in self.morph.parse(word)[1].tag):
          adj = True
        elif 'NOUN' in self.morph.parse(word)[0].tag:
          noun = True
      elif 'NOUN' in self.morph.parse(word)[0].tag and 'nomn' in self.morph.parse(word)[0].tag:
        noun = True
      elif 'NPRO' in self.morph.parse(word)[0].tag:
        pron = True
      elif 'PRTF' in self.morph.parse(word)[0].tag or 'PRTS' in self.morph.parse(word)[0].tag:
        prt = True
      if len(self.morph.parse(word)) > 1:
        if ('VERB' in self.morph.parse(word)[1].tag):
          return True

    if ((noun == True or pron == True) and (adj == True or prt == True or verb == True)):
      return True
    if (noun == True and pron == True):
      return True

    return False
  
  # split by delim and check which pieces are true clauses 
  def separate_by(self,delim,text,subj_required=False):
    '''
    params
    ---
    text : str
    return
    ---
    result : list of str
    '''
    result = []
    cands = [cand for cand in re.split(delim,text) if cand != ' ']
    appended = [False]*len(cands)
    if (len(cands) > 1):
      for i in range(1,len(cands)):
        if self._pred_in(cands[i]) == False:
          if cands[i-1] in result:
            result.remove(cands[i-1])
          result.append(cands[i-1] + delim + cands[i])
          cands[i] = cands[i-1] + delim + cands[i]
          appended[i] = True
          appended[i-1] = True
        else:
          result.append(cands[i])
          appended[i] = True
      if (appended[0] == False):
        if self._pred_in(cands[0]) ==True:
          result.insert(0,cands[0])
        else:
          result[0] = cands[0] + delim + result[0]
      return result
    result = cands
    return result

  def into_clauses(self,text):
    '''
    params
    ---
    text : str
    
    return
    ---
    clauses : list of str 
    '''
    
    # FIRSTLY CHECK INTRODUCTORY PHRASES, e.g. "Ребят, где тут мост?", "Привет, как там с деньгами?"
    introductory_phrase = self.introductory_phrase(text)
    if introductory_phrase != '':
      text = re.sub(introductory_phrase, '', text)

    text = ' ' + text + ' '
    text = re.sub(self.conjs + ' ', '<stop>',text)
    temp = re.findall(self.introductory,text.lower())
    for t in temp:
      if t.capitalize() in text: t = t.capitalize()
      if t.upper() in text: t = t.upper()
      text = text[:text.index(t) - 1] + '<stop>' + text[text.index(t):text.index(t) + len(t)] + '<stop>' + text[text.index(t) + len(t):]
    clauses = text.split('<stop>')
    temp = []

    if ',' in text:
      temp = []
      for clause in clauses:
        for x in self.separate_by(',',clause):
          temp.append(x.strip(' ').strip(','))
      clauses = [x  for x in temp if x != '']

    if ' и ' in text:
      temp = []
      for clause in clauses:
        for x in self.separate_by(' и ',clause):
          temp.append(x.strip(' ').strip(','))
      clauses = [x for x in temp if x != '']

    if ';' in text:
      temp = []
      for clause in clauses:
        for x in self.separate_by(';',clause):
          temp.append(x.strip(' ').strip(','))
      clauses = [x for x in temp if x != '']

    if ':' in text:
      temp = []
      for clause in clauses:
        for x in self.separate_by(':',clause):
          temp.append(x.strip(' ').strip(','))
      clauses = [x for x in temp if x != '']

    if ' - ' in text:
      temp = []
      for clause in clauses:
        for x in self.separate_by('-',clause):
          temp.append(x.strip(' ').strip(','))
      clauses = [x for x in temp if x != '']

    clauses = [clause.strip() for clause in clauses if clause.strip() != '']
    if introductory_phrase != '':
      clauses.insert(0,introductory_phrase)
    return clauses

