import os
import time
import json

import uproot
import numpy as np

from quickstats.components import CLIParser, ExtendedModel, ExtendedMinimizer
from quickstats.utils import root_utils

import ROOT

class NuisanceParameterPull(object):
    _CLI_USAGE_          = 'quickstats run_pulls [-h|--help] [<args>]'
    _CLI_DESCRIPTION_    = 'Tool for computing the impact of a given NP to a set of POIs'    
    _CLI_ARG_OPTIONS_    = \
        {
            'input_file': {
                'abbr'        : 'i',
                'description' : 'Path to the input workspace file',
                'required'    : True,
                'type'        : str
            },
            'workspace':{
                'abbr'        : 'w',
                'description' : 'Name of workspace',
                'required'    : False,
                'type'        : str,
                'default'     : 'combWS'
            },
            'model_config':{
                'abbr'        : 'm',
                'description' : 'Name of model config',
                'required'    : False,
                'type'        : str,
                'default'     : 'ModelConfig'
            },  
            'data':{
                'abbr'        : 'd',
                'description' : 'Name of dataset',
                'required'    : False,
                'type'        : str,
                'default'     : 'combData'
            },
            'parameter'  : {
                'abbr'        : 'p',
                'description' : 'Parameter to run pulls on', 
                'required'    : True,
                'type'        : str,
            },   
            'poi': {
                'abbr'        : 'x',
                'description' : 'POIs to measure',
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },
            'profile': {
                'abbr'        : 'r',
                'description' : 'Parameters to profile', 
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },
            'fix': {
                'abbr'        : 'f',
                'description' : 'Parameters to fix', 
                'required'    : False,
                'type'        : str,
                'default'     : ""
            },
            'snapshot': {
                'abbr'        : 's',
                'description' : 'Name of initial snapshot', 
                'required'    : False,
                'type'        : str,
                'default'     : "nominalNuis"
            },
            'outdir': {
                'abbr'        : 'o',
                'description' : 'Output directory', 
                'required'    : False,
                'type'        : str,
                'default'     : "output"
            },
            'minimizer_type'  : {
                'abbr'        : 't',
                'description' : 'Minimizer type', 
                'required'    : False,
                'type'        : str,
                'default'     : "Minuit2"
            },        
            'minimizer_algo'  : {
                'abbr'        : 'a',
                'description' : 'Minimizer algorithm', 
                'required'    : False,
                'type'        : str,
                'default'     : "Migrad"
            },          
            'num_cpu'  : {
                'abbr'        : 'c',
                'description' : 'Number of CPUs to use', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },   
            'binned'  : {
                'abbr'        : 'b',
                'description' : 'Binned likelihood', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },    
            'precision'  : {
                'abbr'        : 'q',
                'description' : 'Precision for scan', 
                'required'    : False,
                'type'        : float,
                'default'     : 0.001
            },          
            'eps'  : {
                'abbr'        : 'e',
                'description' : 'Convergence criterium', 
                'required'    : False,
                'type'        : float,
                'default'     : 1.0
            },              
            'log_level'  : {
                'abbr'        : 'l',
                'description' : 'Log level', 
                'required'    : False,
                'type'        : str,
                'default'     : "INFO"
            },      
            'eigen'  : {
                'abbr'        : None,
                'description' : 'Compute eigenvalues and vectors', 
                'required'    : False,
                'type'        : int,
                'default'     : 0
            },   
            'strategy'  : {
                'abbr'        : None,
                'description' : 'default strategy', 
                'required'    : False,
                'type'        : int,
                'default'     : 0
            },
            'fix_cache'  : {
                'abbr'        : None,
                'description' : 'Fix StarMomentMorph cache', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },    
            'fix_multi'  : {
                'abbr'        : None,
                'description' : 'Fix MultiPdf level 2', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },            
            'offset'  : {
                'abbr'        : None,
                'description' : 'Offset likelihood', 
                'required'    : False,
                'type'        : int,
                'default'     : 1
            },  
            'optimize'  : {
                'abbr'        : None,
                'description' : 'Optimize constant terms', 
                'required'    : False,
                'type'        : int,
                'default'     : 2
            },       
            'max_calls'  : {
                'abbr'        : None,
                'description' : 'Maximum number of function calls', 
                'required'    : False,
                'type'        : int,
                'default'     : -1
            }, 
            'max_iters'  : {
                'abbr'        : None,
                'description' : 'Maximum number of Minuit iterations', 
                'required'    : False,
                'type'        : int,
                'default'     : -1
            },         
        } 
    
    @property
    def model(self):
        return self._model
    
    @property
    def workspace(self):
        return self._workspace
    @property
    def model_config(self):
        return self._model_config
    @property
    def pdf(self):
        return self._pdf
    @property
    def data(self):
        return self._data
    @property
    def nuisance_parameters(self):
        return self._nuisance_parameters
    @property
    def global_observables(self):
        return self._global_observables
    @property
    def pois(self):
        return self._pois
    @property
    def observables(self):
        return self._observables  
    
    def __init__(self):
        self._model               = None
        self._workspace           = None
        self._model_config        = None
        self._pdf                 = None
        self._data                = None
        self._nuisance_parameters = None
        self._global_observables  = None
        self._pois                = None
        self._observables         = None
    
    def get_parser(self, **kwargs):
        parser = CLIParser(description=self._CLI_DESCRIPTION_,
                           usage=self._CLI_USAGE_)
        parser.load_argument_options(self._CLI_ARG_OPTIONS_)
        return parser
    
    def run_parser(self, args=None):
        parser = self.get_parser()
        kwargs = vars(parser.parse_args(args))
        self.run_pulls(**kwargs)
    
    def load_model(self, **kwargs):
        self._model               = ExtendedModel(**kwargs)
        self._workspace           = self.model.workspace
        self._model_config        = self.model.model_config
        self._pdf                 = self.model.pdf
        self._data                = self.model.data
        self._nuisance_parameters = self.model.nuisance_parameters
        self._global_observables  = self.model.global_observables
        self._pois                = self.model.pois
        self._observables         = self.model.observables
        
    def evaluate_impact(self, nuis, value, pois, minimizer_options, snapshot=None):
        poi_values = []
        start_time = time.time()
        if snapshot:
            self.workspace.loadSnapshot(snapshot)
        nuis.setVal(value)
        nuis.setConstant(1)   
        self.minimizer.minimize(**minimizer_options)
        for poi in pois:
            poi_values.append(poi.getVal())
        elapsed_time = time.time() - start_time
        return poi_values, elapsed_time
        
    def run_pulls(self, input_file='workspace.root', workspace='combWS', model_config='ModelConfig',
                 data='combData', poi='', snapshot='nominalNuis', outdir='output', profile="",
                 fix='', minimizer_type='Minuit2', minimizer_algo='Migrad', num_cpu=1, binned=1,
                 precision=0.001, eps=1.0, log_level='INFO', eigen=0, strategy=0, fix_cache=1, fix_multi=1,
                 offset=1, optimize=2, parameter="", max_calls=-1, max_iters=-1, **kwargs):
        
        start_time = time.time()
        
        # configure default minimizer options
        ExtendedMinimizer._configure_default_minimizer_options(minimizer_type, minimizer_algo,
            strategy, debug_mode=(log_level=="DEBUG"))
        
        # load model
        snapshot_names = snapshot.split(',')
        self.load_model(model_name="model", fname=input_file, ws_name=workspace,
                        model_config_name=model_config, data_name=data, 
                        snapshot_names=snapshot_names, binned_likelihood=binned,
                        tag_as_measurement="pdf_", fix_cache=fix_cache, fix_multi=fix_multi)
        
        # create output directory for pulls results if not exists
        pulls_out_dir = os.path.join(outdir, 'pulls')
        if not os.path.exists(pulls_out_dir):
            os.makedirs(pulls_out_dir)
        
        # fix nuisance parameters at initial values
        if fix:
            self.model.fix_parameters(fix)
                   
        # by default fix all POIs before floating
        self.model.set_parameter_defaults(self.model.pois, error=0.15, constant=1, remove_range=True)
        for param in self.model.pois:
            extra_str = 'Set'
            if param.isConstant():
                extra_str = 'Fixing'
            print('INFO: {} POI {} at value {}'.format(extra_str, param.GetName(), param.getVal()))
        
        # collect pois
        rank_pois = self.model.profile_parameters(poi)
        self.model.set_parameter_defaults(rank_pois, error=0.15)     
        
        # profile pois
        print('INFO: Profiling POIs')
        profile_pois = self.model.profile_parameters(profile)
        
        buffer_time = time.time()
        
        nuip = self.workspace.var(parameter)
        if not nuip:
            raise ValueError('Nuisance parameter "{}" does not exist'.format(parameter))
        nuip_name = nuip.GetName()
        nuip.setConstant(0)
        print('INFO: Computing error for parameter "{}" at {}'.format(nuip.GetName(), nuip.getVal()))
        
        print("INFO: Making ExtendedMinimizer for unconditional fit")
        self.minimizer = ExtendedMinimizer("minimizer", self.pdf, self.data)
        print("INFO: Starting minimization")
        nll_commands = [ROOT.RooFit.NumCPU(num_cpu, 3), 
                        ROOT.RooFit.Constrain(self.nuisance_parameters),
                        ROOT.RooFit.GlobalObservables(self.global_observables), 
                        ROOT.RooFit.Offset(offset)]

        minimize_options = {
            'minimizer_type'   : minimizer_type,
            'minimizer_algo'   : minimizer_algo,
            'default_strategy' : strategy,
            'opt_const'        : optimize,
            'precision'        : precision,
            'eps'              : eps,
            'max_calls'        : max_calls,
            'max_iters'        : max_iters,
        }

        self.minimizer.minimize(nll_commands=nll_commands,
                                scan=1,
                                scan_set=ROOT.RooArgSet(nuip),
                                **minimize_options)
        unconditional_time = time.time() - buffer_time
        print("INFO: Fitting time: {}s".format(unconditional_time))
        pois_hat = []
        for rank_poi in rank_pois:
            name = rank_poi.GetName()
            value = rank_poi.getVal()
            pois_hat.append(value)
            print('{} {}'.format(name, value))
        
        self.workspace.saveSnapshot('tmp_snapshot', self.pdf.getParameters(self.data))
        print('INFO: Made unconditional snapshot with name tmp_snapshot')
        
        # find prefit variation
        buffer_time = time.time()
        
        nuip_hat = nuip.getVal()
        nuip_errup = nuip.getErrorHi()
        nuip_errdown = nuip.getErrorLo()

        all_constraints = self.model.get_all_constraints()
        prefit_variation, constraint_type, nuip_nom = self.model.inspect_constrained_nuisance_parameter(nuip, all_constraints)
        if not constraint_type:
            print('INFO: Not a constrained parameter. No prefit impact can be determined. Use postfit impact instead.')
        prefit_uncertainty_time = time.time() - buffer_time
        print('INFO: Time to find prefit variation: {}s'.format(prefit_uncertainty_time))
        
        if rank_pois:
            new_minimizer_options = {
                'nll_commands': nll_commands,
                'reuse_nll'   : 1,
                **minimize_options
            }
            # fix theta at the MLE value +/- postfit uncertainty and minimize again to estimate the change in the POI
            print('INFO: Evaluating effect of moving {} up by {} + {}'.format(nuip_name, nuip_hat, nuip_errup))
            pois_up, postfit_up_impact_time = self.evaluate_impact(nuip, nuip_hat + abs(nuip_errup), rank_pois,
                                                                   new_minimizer_options,  'tmp_snapshot')
            print('INFO: Time to find postfit up impact: {}s'.format(postfit_up_impact_time))
            
            print('INFO: Evaluating effect of moving {} down by {} - {}'.format(nuip_name, nuip_hat, nuip_errup))
            pois_down, postfit_down_impact_time = self.evaluate_impact(nuip, nuip_hat - abs(nuip_errdown), rank_pois,
                                                                       new_minimizer_options,  'tmp_snapshot')
            print('INFO: Time to find postfit down impact: {}s'.format(postfit_down_impact_time))
            
            # fix theta at the MLE value +/- prefit uncertainty and minimize again to estimate the change in the POI
            
            if constraint_type:
                print('Evaluating effect of moving {} up by {} + {}'.format(nuip_name, nuip_hat, prefit_variation))
                pois_nom_up, prefit_up_impact_time = self.evaluate_impact(nuip, nuip_hat + prefit_variation, rank_pois,
                                                                          new_minimizer_options,  'tmp_snapshot')
                print('INFO: Time to find prefit up impact: {}s'.format(prefit_up_impact_time))      
                
                print('Evaluating effect of moving {} down by {} - {}'.format(nuip_name, nuip_hat, prefit_variation))
                pois_nom_down, prefit_down_impact_time = self.evaluate_impact(nuip, nuip_hat - prefit_variation, rank_pois,
                                                                              new_minimizer_options,  'tmp_snapshot')
                print('INFO: Time to find prefit down impact: {}s'.format(prefit_up_impact_time))
            else:
                print('WARNING: Prefit impact not estimated, instead postfit impact is cloned')
                pois_nom_up = [i for i in pois_up]
                pois_nom_down = [i for i in pois_down]
        else:
        	pois_up, pois_down, pois_nom_up, pois_nom_down = [], [], [], []
        
        end_time = time.time()
        print('\nINFO: Time to perform all fits: {}s'.format(end_time-start_time))
        print('INFO: Unconditional minimum of NP {}: {} + {} - {}'.format(parameter, nuip_hat, 
              abs(nuip_errup), abs(nuip_errdown)))
        print('INFO: Prefit uncertainy of NP {}: {} +/- {}'.format(parameter, nuip_hat, prefit_variation))
        for i, rank_poi in enumerate(rank_pois):
            print('INFO: Unconditional minimum of POI {}: {}'.format(rank_poi.GetName(), pois_hat[i]))
            print('INFO: POI when varying NP up by 1 sigma postfit (prefit): {} ({})'.format(pois_up[i], pois_nom_up[i]))
            print('INFO: POI when varying NP down by 1 sigma postfit (prefit): {} ({})'.format(pois_down[i], pois_nom_down[i]))
        
        # store result in root file
        outname_root = os.path.join(pulls_out_dir, parameter + '.root')
        
        result = {}
        result['nuis'] = {  'nuisance'   : parameter,
                            'nuis_nom'   : nuip_nom,
                            'nuis_hat'   : nuip_hat,
                            'nuis_hi'    : nuip_errup,
                            'nuis_lo'    : nuip_errdown,
                            'nuis_prefit': prefit_variation}
        result['pois'] = {}
        for i, rank_poi in enumerate(rank_pois):
            name = rank_poi.GetName()
            result['pois'][name] = { 'hat'     : pois_hat[i],
                                     'up'      : pois_up[i],
                                     'down'    : pois_down[i],
                                     'up_nom'  : pois_nom_up[i],
                                     'down_nom': pois_nom_down[i]}
            
        result_for_root = {}
        result_for_root.update(result['nuis'])
        for k,v in result['pois'].items():
            buffer = {'{}_{}'.format(k, kk): vv for kk,vv in v.items()}
            result_for_root.update(buffer)
        r_file = ROOT.TFile(outname_root, "RECREATE")
        r_tree = ROOT.TTree("result", "result")
        root_utils.fill_branch(r_tree, result_for_root)
        r_file.Write()
        r_file.Close()
        print('INFO: Saved output to {}'.format(outname_root))
        outname_json = os.path.join(pulls_out_dir, parameter + '.json')
        json.dump(result, open(outname_json, 'w'), indent=2)
    
    @staticmethod
    def parse_root_result(fname):
        with uproot.open(fname) as file:
            result = root_utils.uproot_to_dict(file)
        return result