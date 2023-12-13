class _AttrDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        self[attr] = value

def _payload_cleaner(kwargs: dict, config: dict):
    """Remove Extra Keys for fixing gRPC payloads."""
    
    keys_to_remove = []       
    for k in kwargs.keys():
        if k not in config.keys():
            print("[WARNING] ", k, " key is not in payload/kwargs dict!")
            keys_to_remove.append(k)
    for i in keys_to_remove:
        del kwargs[i]
    return kwargs

def _merge_with_defaults(user_request, default_parameters):
    merged_dict = {**default_parameters, **user_request}

    for key, value in default_parameters.items():
        if key not in user_request:
            merged_dict[key] = value

    return merged_dict

