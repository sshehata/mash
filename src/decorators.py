from functools import wraps

def run_once(method):
  run_var_name = "__"+method.__name__+"_has_run"
  ret_var_name = "__"+method.__name__+"_return"
  @wraps(method)
  def new_f(self, *args, **kwargs):
    if getattr(self, run_var_name, False):
      return getattr(self, ret_var_name)
    setattr(self, run_var_name, True)
    setattr(self, ret_var_name, method(self, *args, **kwargs))
    return getattr(self, ret_var_name)
  return new_f
