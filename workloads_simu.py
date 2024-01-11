import numpy as np

class Workload:
    ''' This class is not meant to be used by itself. It's only purpose
        is to provide definitions that are common to all of its children.
    '''
    # These variables are defined in child classes
    # that inherit from this class. Their definition here is
    # just done for clarity.
    wname = None
    ideal_mem = None
    min_ratio = None
    cpu_req = None

    def __init__(self, idd, percent=0, ratio=0, exp_finish=0):

        self.idd = idd  # a unique uint id for this workload
        self.percent = percent # percent of the work done
        self.ratio = ratio
        self.exp_finish = exp_finish # exp finish time (will remove)
        self.prev_ratio = 0 # keep track of previous ratio (id havn't changed, exp_finsh would be the same)
        self.get_gradient()

    def update_percent(self, el_time):
        self.percent = min(self.percent + el_time/self.profile(self.ratio),1)
        assert self.percent < 1

    def update_ratio(self, new_ratio):
        self.ratio = new_ratio

    def update_exp_finish(self, cur_time):
        self.exp_finish = cur_time + (1-self.percent)*self.profile(self.ratio)

    def update(self, L, sid, cur_time, last_time, new_idd=None, new_ratio=1): # ratio = 0 is no remote memory mode
        if last_time == 0:
            el_time = 0
        else:
            el_time = cur_time - last_time
        assert el_time >= 0, '{},{}'.format(cur_time, last_time)

        if (new_idd is not None) and self.idd == new_idd:
            assert self.percent == 0
        else:
            self.update_percent(el_time)
        self.update_ratio(new_ratio)

        if new_ratio != self.prev_ratio:
            if self.exp_finish > 0:
                L.delete_event(self.exp_finish)
            self.update_exp_finish(cur_time)
            self.exp_finish = L.add_event(self.exp_finish, sid, self.wname, self.idd, False)
            self.prev_ratio = new_ratio

    def set_min_ratio(self, new_min_ratio):
        self.min_ratio = new_min_ratio
        self.min_mem = self.min_ratio * self.ideal_mem

    def get_name(self):
        return self.wname + str(self.idd)

    def compute_ratio_from_coeff(self, coeffs, ratio):
        p = 0
        order = len(coeffs)
        for i in range(order):
            p += coeffs[i] * ratio**(order-1-i)
        return p

    def compute_linear_coeffs(self):
        assert len(self.x) == len(self.y)
        self.a = []
        self.b = []
        for i in range(len(self.y)-1):
            tmp_a =  (self.y[i+1] - self.y[i])/(self.x[i+1] - self.x[i])
            tmp_b =  self.y[i] - tmp_a*self.x[i]
            self.a.append(round(tmp_a,2))
            self.b.append(round(tmp_b,2))

    def profile(self,ratio):
        return self.compute_ratio_from_coeff(self.coeff, ratio)*1000 # from second to millisecond

    def get_gradient(self):
        tmp_coeff = self.coeff + [0]
        self.gd_coeff = np.polyder(self.coeff)
        self.mem_gd_coeff = np.polyder(tmp_coeff)

    def gradient(self, ratio):
        return self.compute_ratio_from_coeff(self.gd_coeff, ratio)

    def mem_gradient(self,ratio):
        return self.compute_ratio_from_coeff(self.mem_gd_coeff, ratio)

class Quicksort(Workload):
    wname = "quicksort"
    ideal_mem = 10300
    min_ratio = 0.7
    min_mem = int(min_ratio * ideal_mem)
    cpu_req = 1
    x = [1,      0.9,    0.8,   0.7,    0.6]
    y = [248.75, 260.41, 268.4, 280.11, 300.78]
    coeff = [-895.83333333, 1814.16666667, -719.04166667, -586.04166667,  635.5]

class Xgboost(Workload):
    wname = "xgboost"
    ideal_mem = 16300
    min_ratio = 0.5
    min_mem = int(min_ratio * ideal_mem)
    cpu_req = 2
    x = [1,      0.9,    0.8,    0.7,    0.6,    0.5,    0.4,    0.3,    0.2]
    y = [338.45, 341.90, 347.52, 349.21, 352.98, 356.92, 386.09, 405.70, 430.11]
    coeff = [ -876.04895105,  1878.74643875, -1148.56526807,    25.39511137, 457.79055556]

class Xsbench(Workload):
    wname = "xsbench"
    ideal_mem = 33300
    min_ratio = 1
    min_mem = int(min_ratio * ideal_mem)
    cpu_req = 8
    x = [1, 0.9, 0.8]
    y = [244.91, 478.54, 10000.0]
    coeff = [-1984.129, 4548.033, -3588.554, 1048.644, 252.997]

class Snappy(Workload):
    wname = "snappy"
    ideal_mem = 34000
    min_ratio = 0.8
    min_mem = int(min_ratio * ideal_mem)
    cpu_req = 1
    x = [1,      0.9,    0.8,    0.7,    0.6]
    y = [134.88, 143.15, 155.37, 211.18, 274.42]
    coeff = [-31583.33333335,  100776.66666673, -118088.66666675,   59796.08333338, -10765.87000001]

class Pagerank(Workload):
    wname = "pagerank"
    ideal_mem = 18900
    min_ratio = 1
    min_mem = int(min_ratio * ideal_mem)
    cpu_req = 8
    x = [1,      0.9,    0.8]
    y = [221.06, 736.29, 99900000.00]
    coeff = [-1617.416, 3789.953, -2993.734, 1225.477]

class Redis(Workload):
    wname = "redis"
    ideal_mem = 31800
    min_ratio = 0.6
    min_mem = int(min_ratio * ideal_mem)
    cpu_req = 2
    x = [1,      0.9,    0.8,    0.7,    0.6,    0.5,    0.4]
    y = [1273.74, 1280.33, 1290.85, 1340.63, 1479.72, 1694.631, 1949.36 ]
    coeff = [-14813.52272727,  38076.50252525, -31906.18749999,   8189.04796176, 1725.16288095]

def get_workload_class(wname):
    return {'quicksort': Quicksort,
            'xgboost': Xgboost,
            'xsbench': Xsbench,
            'pagerank': Pagerank,
            'snappy': Snappy,
            'redis': Redis}[wname]
