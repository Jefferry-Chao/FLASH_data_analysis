# -*- coding: utf-8 -*-
#*************************************************************************
#***File Name: flash_class.py
#***Author: Zhonghai Zhao
#***Mail: zhaozhonghi@126.com 
#***Created Time: 2018年03月25日 星期日 14时39分05秒
#*************************************************************************
# changed some lines.
class flash_class(object):
    '''
    This class contains some function used in flash_visual module.
    '''
    # initialization
    def __init__(self):
        pass
    def line_set(self):
        '''
        This function stored some predefined line plot parameters.
        Parameters:
            None.
        Returns:
            line_list.
        Raises:
            KeyError.
        '''
        line_list = ['r-', 'g--', 'b-.', 'c:', 'k-', 'y--', 'm-.']
        return line_list
    def get_data(self, prefix='lasslab', filenumber=0, keyword='cnt'):
        '''
        This function is used to get file full name.
        Parameters:
            prefix         - FLASH output file prefix.
            filenumber     - FLASH output file number.
            keyword        - FLASH output file keyword.
        Returns:
            data.
        Raises:
            KeyError.
        '''
        import h5py as h5
        if (keyword == 'cnt'):
            s = '_hdf5_plt_cnt_'
        else:
            s = '_hdf5_plt_chk_'
        filename = prefix + s + str(filenumber).zfill(4)
        # read data
        data = h5.File(filename, 'r')

        # return
        return data

    def get_constant(self, field='dens'):
        '''
        This function is used to get normalization constant.
        Parameters:
            field          - physical field.
        Returns:
            constant.
        Raises:
            KeyError.
        '''
        normalize = {'dens':2.7, 'tele':11604505.9491, 'tion':11604505.9491, 'trad':11604505.9491}
        keys = normalize.keys()
        ifinkeys = False
        for each in keys:
            if (each == field):
                constant = normalize[each]
                ifinkeys = True
        if (ifinkeys == True):
            return constant
        else:
            print 'field selected in not in data file.'
            return 1.0
    def get_block(self, data, refine=0, geom=[0.004, 0.008], box_scale=0.8, box_panning=[0.1, 0.1]):
        '''
        This function is used to find out the necessary block to plot.
        Parameters:
            data           - FLASH output file data.
            refine         - refine level.
            box_scale      - total box scale.
            box_panning    - box panning.
            geom           - 2d geometry axis.
        Returns:
            block.
        Raises:
            KeyError.
        '''
        x = geom[0]
        y = geom[1]
        refine_level = data[u'refine level'][:]
        max_level = max(refine_level)
        length = refine_level.shape[0]
        bounding_box = data[u'bounding box'][:]
        block = []
        if (refine == 0):
            #for j in range(max_level, 0, -1):
            for i in range(length):
                if (i != length-1):
                    ifenter_1 = refine_level[i] == max_level
                    ifenter_2 = (refine_level[i+1] <= refine_level[i]) and (refine_level[i] != max_level)
                    ifenter = ifenter_1 or ifenter_2
                else:
                    ifenter = True
                if (ifenter == True):
                    info = [i]
                    info.append(bounding_box[i][0, 0]/x*box_scale + box_panning[0])
                    info.append(bounding_box[i][1, 0]/y*box_scale + box_panning[1])
                    info.append((bounding_box[i][0, 1] - bounding_box[i][0, 0])/x*box_scale)
                    info.append((bounding_box[i][1, 1] - bounding_box[i][1, 0])/y*box_scale)
                    block.append(info)
        else:
            for i in range(length):
                if (refine_level[i] == refine):
                    info = [i]
                    info.append(bounding_box[i][0, 0]/x*box_scale + box_panning[0])
                    info.append(bounding_box[i][1, 0]/y*box_scale + box_panning[1])
                    info.append((bounding_box[i][0, 1] - bounding_box[i][0, 0])/x*box_scale)
                    info.append((bounding_box[i][1, 1] - bounding_box[i][1, 0])/y*box_scale)
                    block.append(info)
        # return
        return block
    def get_line(self, field_data=[], block=[], axis='x', coordinate=0.5, ngrid=16):
        '''
        This function is used to calculate the line-data in FLASH output file.
        Parameters:
            field_data    - FLASH output file data.
            block          - data block.
            axis           - coordinate axis.
            coordinate     - coordinate.
            ngrid          - number of grid in each block.
        Returns:
            array.
        Raises:
            KeyError.
        '''
        import numpy as np

        length = len(block)
        array = []
        for i in range(length):
            n = block[i][0]
            #if_in_block = False
            x0 = block[i][1]
            x1 = block[i][1] + block[i][3]
            y0 = block[i][2]
            y1 = block[i][2] + block[i][4]
            # calculate index
            if (axis == 'x'):
                if (( coordinate >= x0) and (coordinate <= x1)):
                    #if_in_block = True
                    index = int(round((coordinate - x0)/(x1 - x0)*(ngrid - 1)))
                # get data
                #if (if_in_block == True):
                    data_list = []
                    data_list.append(np.linspace(y0, y1, ngrid))
                    data_list.append(field_data[n, 0, :, index])
                    array.append(data_list)
            elif (axis == 'y'):
                if (( coordinate >= y0) and coordinate <= y1):
                    #if_in_block = True
                    index = int(round((coordinate - y0)/(y1 - y0)*(ngrid - 1)))
                # get data
                #if (if_in_block == True):
                    data_list = []
                    data_list.append(np.linspace(x0, x1, ngrid))
                    data_list.append(field_data[n, 0, index, :])
                    array.append(data_list)
            else:
                pass
        return array
    def get_coord(self, axis='x', coordinate=0, geom=[0.004, 0.008], geom_factor=10000, box_scale=0.8, box_panning=[0.1, 0.1]):
        '''
        This function is used to calculate coordinate in figure frame.
        Parameters:
            axis           - coordinate axis.
            coordinate     - coordinate.
            geom           - 2d geometry axis.
            geom_factor    - 2d geometry axis factor.
            box_scale      - total box scale.
            box_panning    - box panning
        Returns:
            coord.
        Raises:
            KeyError.
        '''
        coord = []
        if (axis == 'x'):
            coord.append(coordinate/(geom[0]*geom_factor)*box_scale + box_panning[0])
            coord.append([0, geom[1]*geom_factor])
            coord.append('$ Y/\mu m $')
        elif (axis == 'y'):
            coord.append(coordinate/(geom[1]*geom_factor)*box_scale + box_panning[1])
            coord.append([0, geom[0]*geom_factor])
            coord.append('$ X/\mu m $')
        else:
            pass
        return coord
    def reconstruct(self, array=[], axis='x', ngrid=16, geom=[0.004, 0.008], geom_factor=10000, box_scale=0.8, box_panning=[0.1, 0.1], constant=1.0):
        '''
        This function is used to re-construct line-data in FLASH output file.
        Parameters:
            array          - array to be reconstructed.
            axis           - coordinate axis.
            ngrid          - number of grid in each block.
            geom           - 2d geometry axis.
            geom_factor    - 2d geometry axis factor.
            box_scale      - total box scale.
            box_panning    - box panning.
            constant       - normalization constant.
        Returns:
            re_aeeay.
        Raises:
            KeyError.
        '''
        import numpy as np

        length = len(array)
        if (length == 0):
            print 'Nothing to be reconstructed!'
        else:
            x = []
            y = []
            for j in range(length):
                if (j == 0):
                    for i in range(ngrid-1):
                        x.append(array[j][0][i])
                        y.append(array[j][1][i])
                elif (j == length-1):
                    for i in range(ngrid):
                        if (i == 0):
                            x.append(array[j][0][i])
                            y.append((array[j][1][i] + array[j-1][1][ngrid-1])/2.0)
                        else:
                            x.append(array[j][0][i])
                            y.append(array[j][1][i])
                else:
                    for i in range(ngrid-1):
                        if (i == 0):
                            x.append(array[j][0][i])
                            y.append((array[j][1][i] + array[j-1][1][ngrid-1])/2.0)
                        else:
                            x.append(array[j][0][i])
                            y.append(array[j][1][i])
        # reconstruct x
        if (axis == 'x'):
            x = list((np.array(x) - box_panning[1])/box_scale * geom_factor * geom[1])
        elif (axis == 'y'):
            x = list((np.array(x) - box_panning[0])/box_scale * geom_factor * geom[0])
        else:
            pass
        y = np.array(y)
        return [x, y]
