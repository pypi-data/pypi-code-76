from torch import matmul, nn, reshape, stack, zeros


class Reshape(nn.Module):
    """
    Reshape Module

    Just a helper since PyTorch does not have one.
    """

    def __init__(self, *args):
        super(Reshape, self).__init__()
        self.shape = args

    def forward(self, x):
        return x.view(self.shape)


class GANAttention(nn.Module):
    """
    Custom Attention Module from https://github.com/AdalbertoCq/Pathology-GAN/blob/master/models/generative/ops.py (attention_block)
    """

    def __init__(self, z: tuple(int, int, int), channel_divisor: int):
        """
        Init for GANGAttention

        :param z: input
        :type tuple(int, int, int): input with format of tuple(channels, width, height)
        :param channel_divisor: divisor to calculate f_g_channel (f_g_channel=channels//channel_divisor)
        :type channel_divisor: int
        """

        super(GANAttention, self).__init__()

        def block_conv_spectral(in_channels, out_channels, kernel_size, stride, padding):
            # Conv + spectral norm
            return [nn.utils.spectral_norm(nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size,
                                                     stride=stride, bias=True, padding=padding), n_power_iterations=1, eps=1e-12)]

        self.channels, self.height, self.width = z

        # TODO is required_grad auto set if it is set for calling class?
        self.gamma = zeros(1)

        self.f_g_channels = self.channels//channel_divisor

        self.f = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.f_g_channels, kernel_size=(1, 1), stride=(1, 1), padding=0)
                               )

        self.g = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.f_g_channels, kernel_size=(1, 1), stride=(1, 1), padding=0)
                               )

        self.h = nn.Sequential(*block_conv_spectral(in_channels=self.channels,
                                                    out_channels=self.channels, kernel_size=(1, 1), stride=(1, 1), padding=0)
                               )

        # Initiliaze weights
        self.weights_init()

    def forward(self, x):
        # it was [batch_size, height*width, channels] in tf
        f_flat = reshape(self.f(x), stack(
            [x.size(0), self.f_g_channels, self.height*self.width]))
        g_flat = reshape(self.g(x), stack(
            [x.size(0), self.f_g_channels, self.height*self.width]))
        h_flat = reshape(self.h(x), stack(
            [x.size(0), self.channels, self.height*self.width]))

        s = matmul(g_flat, f_flat, transpose_b=True)

        beta = nn.functional.softmax(s)

        o = matmul(beta, h_flat)
        o = reshape(o, shape=stack(
            [x.size(0), self.channels, self.height, self.width]))
        y = self.gamma*o + x

        return y

    def weights_init(self):
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.orthogonal_(module.weight, gain=1e-4)
                nn.init.constant_(module.bias, 0)
