"""Definition of sicor enmap options schema (as used by cerberus library)."""
sicor_enmap_schema = {
    "sensor": {
        "type": "dict",
        "schema": {
            "name": {
                "type": "string",
                "required": True
            },
            "resamp_alg": {
                "type": "string",
                "required": True
            },
            "fit": {
                "type": "dict",
                "schema": {
                    "idx": {
                        "type": "list",
                        "required": True
                    },
                    "snr": {
                        "type": "list",
                        "required": True
                    }
                }
            }
        }
    },
    "retrieval": {
        "type": "dict",
        "schema": {
            "land_only": {
                "type": "boolean",
                "required": True
            },
            "fn_LUT": {
                "type": "string",
                "required": True,
                "existing_path": True
            },
            "cpu": {
                "type": "integer",
                "required": True
            },
            "disable_progressbars": {
                "type": "boolean",
                "required": True
            },
            "segmentation": {
                "type": "boolean",
                "required": True
            },
            "n_pca": {
                "type": "integer",
                "required": True
            },
            "segs": {
                "type": "integer",
                "required": True
            },
            "default_aot_value": {
                "type": "float",
                "required": True
            },
            "state_vector": {
                "type": "dict",
                "schema": {
                    "water_vapor": {
                        "type": "dict",
                        "schema": {
                            "prior_mean": {
                                "type": "float",
                                "required": True
                            },
                            "use_prior_mean": {
                                "type": "boolean",
                                "required": True
                            },
                            "ll": {
                                "type": "float",
                                "required": True
                            },
                            "ul": {
                                "type": "float",
                                "required": True
                            },
                            "prior_sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    },
                    "intercept": {
                        "type": "dict",
                        "schema": {
                            "prior_mean": {
                                "type": "float",
                                "required": True
                            },
                            "use_prior_mean": {
                                "type": "boolean",
                                "required": True
                            },
                            "ll": {
                                "type": "float",
                                "required": True
                            },
                            "ul": {
                                "type": "float",
                                "required": True
                            },
                            "prior_sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    },
                    "slope": {
                        "type": "dict",
                        "schema": {
                            "prior_mean": {
                                "type": "float",
                                "required": True
                            },
                            "use_prior_mean": {
                                "type": "boolean",
                                "required": True
                            },
                            "ll": {
                                "type": "float",
                                "required": True
                            },
                            "ul": {
                                "type": "float",
                                "required": True
                            },
                            "prior_sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    },
                    "liquid_water": {
                        "type": "dict",
                        "schema": {
                            "prior_mean": {
                                "type": "float",
                                "required": True
                            },
                            "use_prior_mean": {
                                "type": "boolean",
                                "required": True
                            },
                            "ll": {
                                "type": "float",
                                "required": True
                            },
                            "ul": {
                                "type": "float",
                                "required": True
                            },
                            "prior_sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    },
                    "ice": {
                        "type": "dict",
                        "schema": {
                            "prior_mean": {
                                "type": "float",
                                "required": True
                            },
                            "use_prior_mean": {
                                "type": "boolean",
                                "required": True
                            },
                            "ll": {
                                "type": "float",
                                "required": True
                            },
                            "ul": {
                                "type": "float",
                                "required": True
                            },
                            "prior_sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    }
                }
            },
            "unknowns": {
                "type": "dict",
                "schema": {
                    "skyview": {
                        "type": "dict",
                        "schema": {
                            "sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    },
                    "water_vapor_absorption_coefficients": {
                        "type": "dict",
                        "schema": {
                            "sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    },
                    "liquid_water_absorption_coefficients": {
                        "type": "dict",
                        "schema": {
                            "sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    },
                    "ice_absorption_coefficients": {
                        "type": "dict",
                        "schema": {
                            "sigma": {
                                "type": "float",
                                "required": True
                            }
                        }
                    }
                }
            },
            "inversion": {
                "type": "dict",
                "schema": {
                    "gnform": {
                        "type": "string",
                        "required": True
                    },
                    "full": {
                        "type": "boolean",
                        "required": True
                    },
                    "maxiter": {
                        "type": "integer",
                        "required": True
                    },
                    "eps": {
                        "type": "float",
                        "required": True
                    }
                }
            }
        }
    }
}
