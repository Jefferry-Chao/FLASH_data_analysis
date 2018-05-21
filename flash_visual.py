# -*- coding: utf-8 -*-
#*************************************************************************
#***File Name: flash_visual.py
#***Author: Zhonghai Zhao
#***Mail: zhaozhonghi@126.com 
#***Created Time: 2018年03月25日 星期日 14时39分05秒
#*************************************************************************
class flash_visual(object):
    '''
    This class contains some functions to visualize FLASH output data.
    '''
    # initialization
    def __init__(self):
        pass
    def plot_array(self, prefix='lasslab', filenumber=0, keyword='cnt', field='dens', refine=2, vrange=[0, 2.7], box_panning=[0.1, 0.1], box_scale=0.8, geom=[0.004, 0.008], figure_size=(4, 8), geom_factor=10000, ifdisplay=True):
        '''
        This function is used to visualize 2d FLASH output data.
        Parameters:
            prefix         - FLASH output file prefix.
            filenumber     - FLASH output file number.
            keyword        - FLASH output file keyword.
            field          - physical field.
            refine         - refine level.
            vrange         - plot range.
            box_scale      - total box scale.
            box_panning    - box panning
            geom           - 2d geometry axis.
            figure_size    - figure size
            geom_factor    - 2d geometry axis factor.
        Returns:
            None.
        Raises:
            KeyError.
        '''
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        import matplotlib.colors as colors
        import matplotlib.colorbar as colorbar
        import flash_class
        fc = flash_class.flash_class()

        constant = fc.get_constant(field)
        length = len(filenumber)
        for j in range(length):
            data = fc.get_data(prefix=prefix, filenumber=filenumber[j], keyword=keyword)
            field_data = data[field][:]
            block = fc.get_block(data, refine=refine, geom=geom, box_scale=box_scale, box_panning=box_panning)
            n = len(block)
            # plot
            fig = plt.figure(figsize=figure_size)
            plt.axes([box_panning[0], box_panning[1], box_scale, box_scale], xlim=[0, geom[0]*geom_factor], ylim=[0, geom[1]*geom_factor])
            plt.title(field + ' ' + r'$ time = ' + str(filenumber[j]/100.) + ' ns $', fontsize=20)
            plt.xlabel(r'$ X/\mu m $', fontsize=16)
            plt.ylabel(r'$ Y/\mu m $', fontsize=16)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            color_map = cm.RdBu_r
            for i in range(n):
                ax = plt.axes(block[i][1:])
                ax = plt.imshow(field_data[block[i][0], 0, :, :]/constant, origin='lower', cmap=color_map, vmin=vrange[0], vmax=vrange[1])
                plt.xticks([])
                plt.yticks([])
            # add color bar
            color_bar = fig.add_axes([0.2, 0.04, 0.6, 0.02])
            norm = colors.Normalize(vmin=vrange[0], vmax=vrange[1])
            cb = colorbar.ColorbarBase(color_bar, cmap=color_map, norm=norm, orientation="horizontal")
            if (ifdisplay == True):
                plt.show()
            else:
                s1 = 'figure/'
                s2 = field + '_' + str(filenumber[j]).zfill(4) + '.png'
                path = s1 + s2
                plt.savefig(path, dpi=300)
            plt.close()
    def plot_line(self, prefix='lasslab', filenumber=0, keyword='cnt', field='dens', refine=0, vrange=[0, 2.7], box_panning=[0.1, 0.1], box_scale=0.8, geom=[0.004, 0.008], figure_size=(8, 4), geom_factor=10000, axis='x', coordinate=0.5, ngrid=16, ifrecontruct=True, ifdisplay=True):
        '''
        This function is used to visualize 2d FLASH output data.
        Parameters:
            prefix         - FLASH output file prefix.
            filenumber     - FLASH output file number.
            keyword        - FLASH output file keyword.
            field          - physical field.
            refine         - refine level.
            vrange         - plot range.
            box_scale      - total box scale.
            box_panning    - box panning
            geom           - 2d geometry axis.
            figure_size    - figure size
            geom_factor    - 2d geometry axis factor.
            axis           - coordinate axis.
            coordinate     - coordinate.
            ngrid          - number of grid in each block.
            ifdisplay      - if display figure.
        Returns:
            None.
        Raises:
        d5    # plot
            fig = plt.figure(figsize=figure_size)
            plt.title(field + ' ' + r'$ time = ' + str(filenumber[j]/100.) + ' ns $', fontsize=20)
            plt.xlabel(coord[2], fontsize=16)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            KeyError.
        '''
        import matplotlib.pyplot as plt
        import flash_class
        fc = flash_class.flash_class()

        constant = fc.get_constant(field)
        line_list = fc.line_set()
        coord = fc.get_coord(axis=axis, coordinate=coordinate, geom=geom, geom_factor=geom_factor, box_scale=box_scale, box_panning=box_panning)
        length = len(filenumber)
        # plot
        fig = plt.figure(figsize=figure_size)
        plt.title(field + ' ' + axis + ' = ' + str(coordinate), fontsize=20)
        plt.xlabel(coord[2], fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        for j in range(length):
            data = fc.get_data(prefix=prefix, filenumber=filenumber[j], keyword=keyword)
            field_data = data[field][:]
            block = fc.get_block(data, refine=refine, geom=geom, box_scale=box_scale, box_panning=box_panning)
            array = fc.get_line(field_data=field_data, block=block, axis=axis, coordinate=coord[0], ngrid=ngrid)
            if (ifrecontruct == False):
                n = len(array)
                for i in range(n):
                    plt.plot(array[i][0], array[i][1]/constant, linewidth=2)
            else:
                array = fc.reconstruct(array=array, axis=axis, ngrid=ngrid, geom=geom, geom_factor=geom_factor, box_scale=box_scale, box_panning=box_panning, constant=constant)
                legend = 'T = ' + str(filenumber[j]/100.) + ' ns'
                plt.plot(array[0], array[1]/constant, line_list[j], linewidth=2, label=legend)
                plt.legend()
        if (ifdisplay == True):
            plt.show()
        else:
            s1 = 'figure/'
            s2 = 'line_' + field + '_'
            s3 = axis + ' ' + str(coordinate) + '.png'
            path = s1 + s2 + s3
            plt.savefig(path, dpi=300)
        plt.close()
            





