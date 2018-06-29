import pytest

import scedar.qc as qc
import scedar.eda as eda

import numpy as np


class TestFeatureKNNPickUp(object):
    """docstring for TestFeatureKNNPickUp"""
    tx = [[0, 0], [1, 1], [1, 2], [2, 3], [2, 5], [0, 100], [0, 100],
          [0, 101], [10, 100]]
    tsdm = eda.SampleDistanceMatrix(tx, metric="euclidean")

    def run_test_knn_pickup_features(self, nprocs):
        fkp = qc.FeatureKNNPickUp(self.tsdm)
        d = fkp._sdm._d.copy()
        assert d.shape == (9, 9)
        res_sdml = fkp.knn_pickup_features([1, 3, 5], [1, 1, 3],
                                           [0.5, 1.5, 0.5], [1, 1, 5],
                                           nprocs=nprocs)
        assert len(fkp._res_lut) == 3
        assert res_sdml[0]._x.shape == (9, 2)
        assert res_sdml[1]._x.shape == (9, 2)
        assert res_sdml[2]._x.shape == (9, 2)
        assert not np.array_equal(res_sdml[0]._d, d)
        assert not np.array_equal(res_sdml[1]._d, d)
        assert not np.array_equal(res_sdml[2]._d, d)
        # value
        ref_res0 = np.array([[1, 1], [1, 1], [1, 2], [2, 3], [2, 5],
                             [0, 100], [0, 100], [0, 101], [10, 100]])
        np.testing.assert_equal(res_sdml[0]._x, ref_res0)

        ref_res1 = np.array([[2, np.median([2, 3])],
                             [np.median([2]), np.median([2, 3])],
                             [np.median([2]), 2], [2, 3],
                             [2, 5], [10, 100], [10, 100], [10, 101],
                             [10, 100]])
        np.testing.assert_equal(res_sdml[1]._x, ref_res1)

        assert res_sdml[2]._x[0, 0] > 0
        assert res_sdml[2]._x[0, 1] > 0
        assert res_sdml[2]._x[5, 0] > 0
        assert res_sdml[2]._x[6, 0] > 0
        assert res_sdml[2]._x[7, 0] > 0

        # lookup
        np.testing.assert_equal(fkp._res_lut[(1, 1, 0.5, 1, np.median)][0],
                                res_sdml[0]._x)
        np.testing.assert_equal(fkp._res_lut[(3, 1, 1.5, 1, np.median)][0],
                                res_sdml[1]._x)
        np.testing.assert_equal(fkp._res_lut[(5, 3, 0.5, 5, np.median)][0],
                                res_sdml[2]._x)
        # d should not be changed
        np.testing.assert_equal(fkp._sdm._d, d)
        fkp.knn_pickup_features([1, 3, 5], [1, 1, 3],
                                [0.5, 1.5, 0.5], [1, 1, 5],
                                nprocs=nprocs)
        assert len(fkp._res_lut) == 3
        np.testing.assert_equal(fkp._sdm._d, d)
        np.testing.assert_equal(fkp._sdm.x, self.tx)
        # run results should be placed with the correct order
        fkp2 = qc.FeatureKNNPickUp(self.tsdm)
        res1 = fkp2.knn_pickup_features([1, 3, 5], [1, 1, 3],
                                        [0.5, 1.5, 0.5], [1, 1, 5],
                                        nprocs=nprocs)
        fkp3 = qc.FeatureKNNPickUp(self.tsdm)
        res2 = fkp3.knn_pickup_features([2, 3, 4], [1, 1, 3],
                                        [0.5, 1.5, 0.5], [1, 1, 5],
                                        nprocs=nprocs)
        res3 = fkp2.knn_pickup_features([2, 3, 4], [1, 1, 3],
                                        [0.5, 1.5, 0.5], [1, 1, 5],
                                        nprocs=nprocs)
        np.testing.assert_equal(res1[1]._x, res3[1]._x)
        np.testing.assert_equal(res2[0]._x, res3[0]._x)
        np.testing.assert_equal(res2[2]._x, res3[2]._x)

    def test_knn_pickup_features(self):
        self.run_test_knn_pickup_features(1)
        self.run_test_knn_pickup_features(3)

    def test_knn_pickup_features_single_run(self):
        fkp = qc.FeatureKNNPickUp(self.tsdm)
        d = fkp._sdm._d.copy()
        assert d.shape == (9, 9)
        res_sdml = fkp.knn_pickup_features([8], [3], [0.5], [10])

        fkp2 = qc.FeatureKNNPickUp(self.tsdm)
        res_sdml2 = fkp2.knn_pickup_features(8, 3, 0.5, 10)
        np.testing.assert_equal(res_sdml2[0]._x, res_sdml[0]._x)

    def test_knn_pickup_features_stat_fun(self):
        fkp = qc.FeatureKNNPickUp(self.tsdm)
        d = fkp._sdm._d.copy()
        assert d.shape == (9, 9)
        res_sdml = fkp.knn_pickup_features([8], [3], [0.5], [10])

        res_sdml2 = fkp.knn_pickup_features(8, 3, 0.5, 10, 1, np.median)
        np.testing.assert_equal(res_sdml2[0]._x, res_sdml[0]._x)
        assert len(fkp._res_lut) == 1

        res_sdml3 = fkp.knn_pickup_features(8, 3, 0.5, 10, 1,
                                            lambda x: np.median(x))
        np.testing.assert_equal(res_sdml3[0]._x, res_sdml[0]._x)
        assert len(fkp._res_lut) == 2

        res_sdml4 = fkp.knn_pickup_features(8, 3, 0.5, 10, 1,
                                            lambda x: np.median(x))
        np.testing.assert_equal(res_sdml4[0]._x, res_sdml[0]._x)
        assert len(fkp._res_lut) == 3

        res_sdml5 = fkp.knn_pickup_features(8, 3, 0.5, 10, 1, np.min)
        assert not np.array_equal(res_sdml5[0]._x, res_sdml[0]._x)
        assert len(fkp._res_lut) == 4

        res_sdml6 = fkp.knn_pickup_features(
            8, 3, 0.5, 10, 1, lambda x: np.min(x))
        np.testing.assert_equal(res_sdml5[0]._x, res_sdml6[0]._x)
        assert len(fkp._res_lut) == 5

    def test_knn_pickup_features_wrong_args(self):
        fkp = qc.FeatureKNNPickUp(self.tsdm)
        # Invalid parameters
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(0, 1, 10, 1)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, 0, 10, 1)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, 1, 10, 0)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, 1, 10, 0.5)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(0.5, 1, 10, 1)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, -0.1, 10, 1)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, 1, 1, 10, 0.5)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(9, 1, 1, 10, 1)
        # invalid stats funcs
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features([1, 3, 5], [1, 1, 3],
                                    [0.5, 1.5, 0.5], [1, 1, 5],
                                    1, 1)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features([1, 3, 5], [1, 1, 3],
                                    [0.5, 1.5, 0.5], [1, 1, 5],
                                    1, np.array)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features([1, 3, 5], [1, 1, 3],
                                    [0.5, 1.5, 0.5], [1, 1, 5],
                                    1, lambda x, y: x + y)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features([1, 3, 5], [1, 1, 3],
                                    [0.5, 1.5, 0.5], [1, 1, 5],
                                    1, lambda x, y: x + y)
        # Parameters of different length
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features([1, 2], 1, 10, 1)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, [1, 2], 10, 1)
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, 1, 10, [1, 2])
        with pytest.raises(ValueError) as excinfo:
            fkp.knn_pickup_features(1, 1, [10, 20], 1)
