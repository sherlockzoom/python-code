import gdal
import fire
gdal.AllRegister()
import matplotlib.pyplot as plt
import numpy as np
import time

class Config:
    tif_path = "your_path"
    minxy = (80000, 80000)
    im_size = (6000, 6000)
    outdir = 'output'


def min_max_scaler(arr, feature_range=(0,1)):
    return (arr - feature_range[0])/(feature_range[1] - feature_range[0])

def parse_tif():
    tif_data = gdal.Open(opt.tif_path)
    w, h = tif_data.RasterXSize, tif_data.RasterYSize
    bands = tif_data.RasterCount
    print("w: {}, h: {}, brands: {}".format(w,h,bands))
    # vmin = r.GetMinimum()

    r = tif_data.GetRasterBand(1)
    g = tif_data.GetRasterBand(2)
    b = tif_data.GetRasterBand(3)

    nir = tif_data.GetRasterBand(4)
    # 获取地图roi区域
    # min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 255))

    b_part = b.ReadAsArray(opt.minxy[0], opt.minxy[1], opt.im_size[0], opt.im_size[1])
    r_part = r.ReadAsArray(opt.minxy[0], opt.minxy[1], opt.im_size[0], opt.im_size[1])
    g_part = g.ReadAsArray(opt.minxy[0], opt.minxy[1], opt.im_size[0], opt.im_size[1])

    # b_part = min_max_scaler.fit_transform(b_part)
    # r_part = min_max_scaler.fit_transform(r_part)
    # g_part = min_max_scaler.fit_transform(g_part)
    print(b_part.min(), b_part.max())
    b_part = min_max_scaler(b_part, (b_part.min(), b_part.max()))
    r_part = min_max_scaler(r_part, (r_part.min(), r_part.max()))
    g_part = min_max_scaler(g_part, (g_part.min(), g_part.max()))



    nir_part = nir.ReadAsArray(opt.minxy[0], opt.minxy[1], opt.im_size[0], opt.im_size[1])

    nir_part = min_max_scaler(nir_part, (nir_part.min(), nir_part.max()))

    # nir_part = min_max_scaler.fit_transform(nir_part)

    ndwi = (g_part - nir_part)/(g_part + nir_part)


    b_r_g = None
    # print(b_r_g.shape)

    # print(np.expand_dims(b_part, axis=2).shape)
    import os
    if not os.path.exists(opt.outdir):
        os.makedirs(opt.outdir)
    # plt.imshow(b_part)
    #
    plt.imsave('{}/{}_b_test.png'.format(opt.outdir, time.time()), b_part)
    plt.imsave('{}/{}_r_test.png'.format(opt.outdir, time.time()), r_part)
    plt.imsave('{}/{}_g_test.png'.format(opt.outdir, time.time()), g_part)
    #
    r_part = r_part.reshape(opt.im_size[0],opt.im_size[1],1)
    g_part = g_part.reshape(opt.im_size[0],opt.im_size[1],1)
    b_part = b_part.reshape(opt.im_size[0],opt.im_size[1],1)

    b_r_g = [np.expand_dims(arr, axis=2) for arr in [r_part, g_part, b_part]]

    b_r_g = np.concatenate((b_part,g_part, r_part), axis=2)

    plt.imsave('{}/{}_r_b_g.png'.format(opt.outdir, time.time()), b_r_g)
    plt.imsave("{}/{}_ndwi.png".format(opt.outdir, time.time()), ndwi)

    # plt.imsave("ni_part.png", ni_part)
    plt.show()

def main():
    opt = fire.Fire(Config)
    data = gdal.Open(opt.tif_path)

    print(dir(data))
    print(data.GetMetadata())
    print(getattr(data, 'RasterXSize'))

if __name__ == '__main__':
    opt = Config()
    parse_tif()
