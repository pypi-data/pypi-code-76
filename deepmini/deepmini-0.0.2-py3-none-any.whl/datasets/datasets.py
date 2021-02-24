import torch
import matplotlib.pyplot as plt

class MPSC:
    def __init__(
        self,
        num_data=50000,
        data_length=1, # Seconds
        data_rate=1000, # Hz
        amplitude_range=[5, 50], # pA
        frequency_range=[1, 10], # Hz
        rise_tau_range=[0, 0.01], # Seconds
        decay_tau_range=[0.02, 0.05], # d_tau>r_tau
        baseline_range=[0, 100], # pA
        gaussian_noise_range=[0, 0.5], # pA
        sinewave_noise_range=[0, 0.1], # pA
        poisson_events=True,
        poisson_refractory_period=None,
        include_no_event_trace=False,
        random_seed=0,
    ):
        """Generates MPSC Dataset
        
        :param int num_data: total number of dataset to generate. (inputs, targets)
        :param int data_length: (sec) length of trace
        :param int data_rate: (Hz) sampling rate of trace
        :param list amplitude_range: (pA) range of event amplitude. requires list of [min, max]
        :param list frequency_range: (Hz) range of event frequency. requires list of [min, max]
        :param list rise_tau_range: (sec) range of event rise tau. requires list of [min, max]
        :param list decay_tau_range: (sec) range of event decay tau. requires list of [min, max]
        :param list baseline_range: (pA) range of background baseline. requires list of [min, max]
        :param list gaussian_noise_range: (pA) range of background gaussian noise. requires list of [min, max]
        :param list sinewave_noise_range: (pA) range of background sinewave noise. requires list of [min, max]
        :param bool poisson_events: {True|False} if True, generates events by poisson process. else uniform random interval
        :param float poisson_refractory_period: (sec) {None|(float)} if None, refractory periods is Nyquist interval of data_rate.
        :param bool include_no_event_trace: {True|False} if True, dataset might contain None in targets.
        """
        self.num_data=num_data
        self.data_length=data_length
        self.data_rate=data_rate
        self.amplitude_range=amplitude_range
        self.frequency_range=frequency_range
        self.rise_tau_range=rise_tau_range
        self.decay_tau_range=decay_tau_range
        assert rise_tau_range[1]<decay_tau_range[0], 'minimum decay tau should be bigger than maximum rise tau'
        self.baseline_range=baseline_range
        self.gaussian_noise_range=gaussian_noise_range
        self.sinewave_noise_range=sinewave_noise_range
        self.poisson_events = poisson_events
        if poisson_refractory_period is None:
            self.poisson_refractory_period=10/self.data_rate
        self.include_no_event_trace=include_no_event_trace
        torch.manual_seed(random_seed)
        
        self._params = None
        self._inputs = None
        self._targets = None
        self.run()
    
    def run(self):
        self._params = self.get_params()
        self._inputs = self.get_inputs()
        self._targets = self.get_targets()
    
    @property
    def params(self):
        return self._params
    
    @property
    def inputs(self):
        return self._inputs
    
    @property
    def targets(self):
        return self._targets
    
    def get_params(self):
        params = []
        for i in range(self.num_data):
            params.append(self._get_param())
        return params
    
    def get_inputs(self):
        inputs = []
        for param in self.params:
            inputs.append(self._get_input(param))
        return inputs
    
    def get_targets(self):
        targets = []
        for param in self.params:
            targets.append(self._get_target(param))
        return targets
        
    def _get_param(self):
        a_min, a_max = self.amplitude_range
        f_min, f_max = self.frequency_range
        r_min, r_max = self.rise_tau_range
        d_min, d_max = self.decay_tau_range
        b_min, b_max = self.baseline_range
        g_min, g_max = self.gaussian_noise_range
        s_min, s_max = self.sinewave_noise_range
        frequency = torch.rand(1)*(f_max-f_min)+f_min
        expected_num_event = torch.ceil(frequency*self.data_length).to(int)
        
        if self.poisson_events:
            # http://lumiere.ens.fr/~dmarti01/software/dayan_abbott/problem2.html
            iei = -torch.log(torch.rand(expected_num_event))/frequency
            x = iei.cumsum(dim=0)*self.data_length
            if self.poisson_refractory_period:
                x = self._thinning(x)
            x = x[x<self.data_length]
            num_event = x.numel()
            xpos = x*self.data_length
            if num_event==0 and not self.include_no_event_trace:
                num_event = 1
                xpos = torch.rand(1)*self.data_length
            
        else:
            # uniform
            num_event = expected_num_event
            xpos = torch.rand(num_event).sort().values*self.data_length
        
        param= dict(
            freq = frequency,
            nevt = num_event,
            xpos = xpos,
            ypos = torch.rand(num_event)*(a_max-a_min)+a_min,
            rtau = torch.rand(num_event)*(r_max-r_min)+r_min,
            dtau = torch.rand(num_event)*(d_max-d_min)+d_min,
            base = torch.rand(1)*(b_max-b_min)+b_min,
            gaussian = torch.rand(1)*(g_max-g_min)+g_min,
            sinewave = torch.rand(1)*(s_max-s_min)+s_min,
        )
        param['xinit'], param['yinit']=self._peak_to_init(param['xpos'], param['ypos'], param['rtau'], param['dtau'])
        param['x'], param['y'] = None, None
        return param
    
    def _get_input(self, param):
        x = torch.arange(0, self.data_length, 1/self.data_rate)
        y = torch.zeros(x.numel())
        if param['nevt']>=1:
            X = torch.vstack([x]*param['nevt']).T
            Y = param['ypos']*(-torch.exp(-torch.clamp(X-param['xinit'], 0)/param['rtau'])+torch.exp(-torch.clamp(X-param['xinit'], 0)/param['dtau']))
            y += Y.sum(axis=1)
        y += param['base']
        pi = torch.acos(torch.zeros(1)).item()
        fr = torch.rand(1)*10+50
        y += param['sinewave']*torch.sin(2*pi*fr*x)
        y += torch.normal(0, param['gaussian'].item(), size=(len(x),))
        param['x'], param['y'] = x, y
        return torch.vstack([x,y])
    
    def _get_target(self, param):
        if param['nevt']>=1:
            x, y = param['x'], param['y']
            y1 = (y.clone()-param['base']).abs()
            y1[:-1]=y[1:]

            x_init = (param['xinit']*self.data_rate).to(int)
            x_peak = (param['xpos']*self.data_rate).to(int)

            d_init = torch.vstack([y[x_init], y1[x_init]]).min(dim=0).indices
            d_peak = torch.vstack([y[x_peak], y1[x_peak]]).max(dim=0).indices

            vx = x[x_init+d_init]
            vy = y[x_init+d_init]
            ux = x[x_peak+d_peak]
            uy = y[x_peak+d_peak]
            return torch.stack([vx, vy, ux, uy]).T
        else:
            return None
        
    @staticmethod
    def _peak_to_init(ux, uy, t1, t2):
        r = t2/t1
        a = 1/(1-r)
        b = r*a
        dx = b*torch.log(r)*t1
        dy = r**a-r**b
        vx = ux+dx
        vy = uy/dy
        return vx, vy
    
    def _thinning(self, x):
        if len(x)==0:
            return x
        x_new = []
        x_new.append(x[0])
        last_event = x_new[-1]

        v = torch.rand(x.numel() - 1)
        for i, t in enumerate(x[1:]):
            
            z = 1 - torch.exp(-(t - last_event) / self.poisson_refractory_period)
            if (v[i] < z):
                x_new.append(x[i+1])
                last_event = x_new[-1]
            else:
                continue

        x_new = torch.tensor(x_new)
        return x_new
    
    def plot(self, indices=[0]):
        """Plot input and target data with given indices

        :param list indices: 
        ::

            mpsc = MPSC()
            mpsc.plot([10, 235, 5220, 48020])
            mpsc.plot(range(0, 10))
        """
        for i in indices:
            x, y = self.inputs[i]
            plt.plot(x, y, 'k', linewidth=1)
            plt.plot(self.targets[i][:,0], self.targets[i][:,1], 'bx', label='inits')
            plt.plot(self.targets[i][:,2], self.targets[i][:,3], 'rx', label='peaks')
            plt.xlabel('Time (sec)')
            plt.ylabel('Amplitudes (pA)')
            plt.legend()
            plt.show()
    