import numpy as np
import seaborn as sns
import scedar.eda as eda
import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest


class TestSampleFeatureMatrix(object):
    """docstring for TestSampleFeatureMatrix"""
    sfm5x10_arr = np.random.ranf(50).reshape(5, 10)
    sfm3x3_arr = np.random.ranf(9).reshape(3, 3)
    sfm5x10_lst = list(map(list, np.random.ranf(50).reshape(5, 10)))
    plt_sdm = eda.SampleFeatureMatrix(np.arange(60).reshape(6, 10), 
                                      sids=list("abcdef"), 
                                      fids=list(map(lambda i: 'f{}'.format(i), 
                                                    range(10))))


    def test_init_x_none(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(None)

    def test_init_x_bad_type(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix([[0, 1], ['a', 2]])

    def test_init_x_1d(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix([1, 2, 3])

    def test_init_dup_sfids(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(self.sfm5x10_lst, [0, 0, 1, 2, 3])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm5x10_lst, ['0', '0', '1', '2', '3'])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(self.sfm5x10_lst, None, [0, 0, 1, 2, 3])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(self.sfm5x10_lst, None, [
                                    '0', '0', '1', '2', '3'])

    def test_init_empty_x_sfids(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(np.array([[], []]), [])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(np.array([[], []]), None, [])

    def test_init_wrong_sid_len(self):
        # wrong sid size
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm5x10_lst, list(range(10)), list(range(5)))

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(self.sfm5x10_lst, list(range(10)))

    def test_init_wrong_fid_len(self):
        # wrong fid size
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm5x10_lst, list(range(5)), list(range(2)))

    def test_init_wrong_sfid_len(self):
        # wrong sid and fid sizes
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm5x10_lst, list(range(10)), list(range(10)))

    def test_init_non1d_sfids(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(self.sfm3x3_arr, np.array([[0], [1], [2]]),
                                    np.array([[0], [1], [1]]))

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(self.sfm3x3_arr, np.array([[0], [1], [2]]),
                                    np.array([0, 1, 2]))

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(self.sfm3x3_arr, np.array([0, 1, 2]),
                                    np.array([[0], [1], [2]]))

    def test_init_bad_sid_type(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, [False, True, 2], [0, 1, 1])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, [[0], [0, 1], 2], [0, 1, 1])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, np.array([0, 1, 2]), [0, 1, 1])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, [(0), (0, 1), 2], [0, 1, 1])

    def test_init_bad_fid_type(self):
        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, [0, 1, 2], [False, True, 2])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, [0, 1, 2], [[0], [0, 1], 2])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, [0, 1, 2], [(0), (0, 1), 2])

        with pytest.raises(Exception) as excinfo:
            eda.SampleFeatureMatrix(
                self.sfm3x3_arr, [0, 1, 2], np.array([0, 1, 2]))

    def test_valid_init(self):
        eda.SampleFeatureMatrix(
            self.sfm5x10_arr, list(range(5)), list(range(10)))
        eda.SampleFeatureMatrix(self.sfm5x10_arr, None, list(range(10)))
        eda.SampleFeatureMatrix(self.sfm5x10_arr, list(range(5)), None)
        eda.SampleFeatureMatrix(np.arange(10).reshape(-1, 1))
        eda.SampleFeatureMatrix(np.arange(10).reshape(1, -1))

    def test_ind_x(self):
        sids = list("abcdef")
        fids = list(range(10, 20))
        sdm = eda.SampleFeatureMatrix(
            np.random.ranf(60).reshape(6, -1), sids=sids, fids=fids)
        # select sf
        ss_sdm = sdm.ind_x([0, 5], list(range(9)))
        assert ss_sdm._x.shape == (2, 9)
        assert ss_sdm.sids == ['a', 'f']
        assert ss_sdm.fids == list(range(10, 19))

        # select with Default
        ss_sdm = sdm.ind_x()
        assert ss_sdm._x.shape == (6, 10)
        assert ss_sdm.sids == list("abcdef")
        assert ss_sdm.fids == list(range(10, 20))
        
        # select with None
        ss_sdm = sdm.ind_x(None, None)
        assert ss_sdm._x.shape == (6, 10)
        assert ss_sdm.sids == list("abcdef")
        assert ss_sdm.fids == list(range(10, 20))
                        
        # select non-existent inds
        with pytest.raises(IndexError) as excinfo:
            sdm.ind_x([6])

        with pytest.raises(IndexError) as excinfo:
            sdm.ind_x(None, ['a'])

        # select 0 ind
        # does not support empty matrix
        with pytest.raises(ValueError) as excinfo:
            sdm.ind_x([])

        with pytest.raises(ValueError) as excinfo:
            sdm.ind_x(None, [])

    def test_id_x(self):
        sids = list("abcdef")
        fids = list(range(10, 20))
        sdm = eda.SampleFeatureMatrix(
            np.random.ranf(60).reshape(6, -1), sids=sids, fids=fids)
        # select sf
        ss_sdm = sdm.id_x(['a', 'f'], list(range(10, 15)))
        assert ss_sdm._x.shape == (2, 5)
        assert ss_sdm.sids == ['a', 'f']
        assert ss_sdm.fids == list(range(10, 15))

        # select with Default
        ss_sdm = sdm.id_x()
        assert ss_sdm._x.shape == (6, 10)
        assert ss_sdm.sids == list("abcdef")
        assert ss_sdm.fids == list(range(10, 20))
        
        # select with None
        ss_sdm = sdm.id_x(None, None)
        assert ss_sdm._x.shape == (6, 10)
        assert ss_sdm.sids == list("abcdef")
        assert ss_sdm.fids == list(range(10, 20))
                        
        # select non-existent inds
        # id lookup raises ValueError
        with pytest.raises(ValueError) as excinfo:
            sdm.id_x([6])

        with pytest.raises(ValueError) as excinfo:
            sdm.id_x(None, ['a'])

        # select 0 ind
        # does not support empty matrix
        with pytest.raises(ValueError) as excinfo:
            sdm.id_x([])

        with pytest.raises(ValueError) as excinfo:
            sdm.id_x(None, [])

    @pytest.mark.mpl_image_compare
    def test_s_ind_regression_scatter_ax(self):
        fig, axs = plt.subplots(ncols=2)
        fig = self.plt_sdm.s_ind_regression_scatter(
            0, 1, figsize=(5, 5), ax=axs[0])
        plt.close()
        return fig

    @pytest.mark.mpl_image_compare
    def test_s_ind_regression_scatter(self):
        return self.plt_sdm.s_ind_regression_scatter(0, 1, figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_s_id_regression_scatter(self):
        return self.plt_sdm.s_id_regression_scatter("a", "b", 
                                           feature_filter=[1,2,3],
                                           figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_s_ind_regression_scatter_custom_labs(self):
        return self.plt_sdm.s_ind_regression_scatter(0, 1, xlab='X', ylab='Y', 
                                            figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_s_ind_regression_scatter_custom_bool_ff(self):
        return self.plt_sdm.s_ind_regression_scatter(
            0, 1, feature_filter=[True]*2 + [False]*8, figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_s_ind_regression_scatter_custom_int_ff(self):
        return self.plt_sdm.s_ind_regression_scatter(
            0, 1, feature_filter=[0, 1], figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_s_ind_regression_scatter_custom_func_ff(self):
        return self.plt_sdm.s_ind_regression_scatter(
            0, 1, feature_filter=lambda x, y: (x in (0, 1, 2)) and (10 < y < 12), 
            figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_f_ind_regression_scatter_custom_func_sf(self):
        # array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
        #        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        #        [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        #        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        #        [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        #        [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]])
        return self.plt_sdm.f_ind_regression_scatter(
            0, 1, sample_filter=lambda x, y: (x in (0, 10, 20)) and (10 < y < 30), 
            figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_f_ind_regression_scatter_no_ff(self):
        return self.plt_sdm.f_ind_regression_scatter(0, 1, figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_f_ind_regression_scatter_ind_ff(self):
        return self.plt_sdm.f_ind_regression_scatter(0, 1, sample_filter=[0, 2, 5], 
                                            figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    def test_f_ind_regression_scatter_labs(self):
        return self.plt_sdm.f_ind_regression_scatter(0, 1, sample_filter=[0, 2, 5], 
                                            figsize=(5, 5), title='testregscat',
                                            xlab='x', ylab='y')

    @pytest.mark.mpl_image_compare
    def test_f_id_regression_scatter(self):
        return self.plt_sdm.f_id_regression_scatter(
            'f5', 'f6', sample_filter=[0, 2, 5], figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_s_ind_dist_ax(self):
        fig, axs = plt.subplots(ncols=2)
        fig = self.plt_sdm.s_ind_dist(0, figsize=(5, 5), ax=axs[0])
        plt.close()
        return fig

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_s_ind_dist(self):
        return self.plt_sdm.s_ind_dist(0, figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_s_id_dist(self):
        return self.plt_sdm.s_id_dist("a", feature_filter=[1,2,3], 
                                      figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_s_ind_dist_custom_labs(self):
        return self.plt_sdm.s_ind_dist(0, xlab='X', ylab='Y', figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_s_ind_dist_custom_bool_ff(self):
        return self.plt_sdm.s_ind_dist(
            0, feature_filter=[True]*2 + [False]*8, title='testdist',
            figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_s_ind_dist_custom_int_ff(self):
        return self.plt_sdm.s_ind_dist(
            0, feature_filter=[0, 1], figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_s_ind_dist_custom_func_ff(self):
        return self.plt_sdm.s_ind_dist(
            0, feature_filter=lambda x: x in (0, 1, 2), 
            figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_f_ind_dist_custom_func_sf(self):
        return self.plt_sdm.f_ind_dist(
            0, sample_filter=lambda x: x in (0, 10, 20), 
            figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_f_ind_dist_no_ff(self):
        return self.plt_sdm.f_ind_dist(0, figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_f_ind_dist_ind_ff(self):
        return self.plt_sdm.f_ind_dist(0, sample_filter=[0, 2, 5], 
                                       figsize=(5, 5))

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_f_ind_dist_labs(self):
        return self.plt_sdm.f_ind_dist(0, sample_filter=[0, 2, 5], 
                                       figsize=(5, 5), 
                                       xlab='x', ylab='y')

    @pytest.mark.mpl_image_compare
    @pytest.mark.filterwarnings("ignore:The 'normed' kwarg is depreca")
    def test_f_id_dist(self):
        return self.plt_sdm.f_id_dist('f5', sample_filter=[0, 2, 5], 
                                      figsize=(5, 5))

    def test_getters(self):
        tsfm = eda.SampleFeatureMatrix(np.arange(10).reshape(5, 2),
                                       ['a', 'b', 'c', '1', '2'],
                                       ['a', 'z'])

        np.testing.assert_equal(tsfm.x, np.array(
            np.arange(10).reshape(5, 2), dtype='float64'))
        np.testing.assert_equal(tsfm.sids, np.array(['a', 'b', 'c', '1', '2']))
        np.testing.assert_equal(tsfm.fids, np.array(['a', 'z']))

        assert tsfm.x is not tsfm._x
        assert tsfm.sids is not tsfm._sids
        assert tsfm.fids is not tsfm._fids