import numpy
import os, subprocess, sys


def new_get_data(start, end, im_bin_size, raw_file, pusher, function_no, scan_start, scan_end, dir=None):
    if dir is None:
        cdcreader_path = os.getcwd()
    else:
        cdcreader_path = dir

    cdcexe = os.path.join(cdcreader_path, 'CDCReader.exe')
    if not os.path.isfile(cdcexe):
        cdcexe = os.path.join(cdcreader_path, 'unidec_bin', 'CDCReader.exe')
        if not os.path.isfile(cdcexe):
            print "Unable to find CDCReader.exe"
            print cdcexe
            sys.exit()

    if os.path.isfile(cdcexe):
        immsfile = os.path.splitext(raw_file)[0] + '_' + str(function_no) + '_imms.txt'
        msfile = os.path.splitext(raw_file)[0] + '_' + str(function_no) + '_ms.txt'
        print "IMMS Processing: ", raw_file
        print "Outputs:\n\t", immsfile, "\n\t", msfile

        call_params = [cdcexe,
                       "-r", raw_file,
                       "-m", msfile,
                       "-i", immsfile,
                       "--im_bin=" + str(im_bin_size),
                       "--fn=" + function_no,
                       "--ms_smooth_window=0",
                       "--ms_number_smooth=0",
                       "--ms_bin=" + str(im_bin_size)]

        if scan_start > 0.:
            call_params.append("--scan_start=" + str(scan_start))

        if scan_end is not None and scan_end > 0.:
            call_params.append("--scan_end=" + str(scan_end))
        try:
            call_params.append("--mass_start=" + str(int(start)))
            call_params.append("--mass_end=" + str(int(end)))
        except ValueError:
            pass

        p = subprocess.call(call_params, shell=False)  # , stdout=devnull, shell=False)

        if p != 0:
            print "CONVERSION ERROR! Call Parameters:", call_params
            print "Std out", p

        try:
            '''
            # This allows the data to be imported if you wanted to use it
            # msfile=raw_file + '_' + str(function_no) + '_ms.txt'
            ms_data = numpy.loadtxt(msfile, dtype='float')
            A = ms_data[:, 0]
            B = ms_data[:, 1]

            # immsfile=raw_file + '_' + str(function_no) + '_imms.txt'
            imms_data = numpy.loadtxt(immsfile, dtype='float')
            mymap2 = dict((mz_value, numpy.zeros(200)) for mz_value in numpy.unique(imms_data[:, 0]))

            for row in imms_data:
                mymap2[row[0]][row[1]] = row[2]

            mz_values = mymap2.keys()
            mz_values.sort()
            if pusher is not None:
                arrival_times = numpy.array(range(200)) * (float(pusher) / 1000.)
            else:
                arrival_times = numpy.array(range(200))
                print "No Pusher Provided, Using Bin Number"

            X, Y, C = [], [], []
            for mz in mz_values:
                X.append(numpy.ones(200) * mz)
                Y.append(arrival_times)
                C.append(mymap2[mz])

            X = numpy.array(X)
            Y = numpy.array(Y)
            C = numpy.array(C)

            return A, B, X, Y, C
            '''
            return None, None, None, None, None
        except Exception, e:
            print "ERROR"
            print e
            return None, None, None, None, None


def new_get_data_MS(start, end, bin_size, raw_file, function_no, scan_start, scan_end, dir=None):
    if dir is None:
        reader_path = os.getcwd()
    else:
        reader_path = dir

    rawexe = os.path.join(reader_path, 'rawreadertim.exe')

    if not os.path.isfile(rawexe):
        rawexe = os.path.join(reader_path, "unidec_bin", 'rawreadertim.exe')
        if not os.path.isfile(rawexe):
            print "Unable to find rawreadertim.exe"
            print rawexe
            sys.exit()

    if os.path.isfile(rawexe):
        msfile = os.path.splitext(raw_file)[0] + '_' + str(function_no) + '_ms.txt'
        print "MS Processing: ", raw_file, "to", msfile

        call_params = [rawexe,
                       "-r", raw_file,
                       "-m", msfile,
                       "--fn=" + function_no,
                       "--ms_smooth_window=0",
                       "--ms_number_smooth=0",
                       "--ms_bin=" + str(bin_size)]

        if scan_start > 0.:
            call_params.append("--scan_start=" + str(scan_start))

        if scan_end is not None and scan_end > 0.:
            call_params.append("--scan_end=" + str(scan_end))

        try:
            call_params.append("--mass_start=" + str(int(start)))
            call_params.append("--mass_end=" + str(int(end)))
        except ValueError:
            pass

        p = subprocess.call(call_params, shell=False)

        if p != 0:
            print "CONVERSION ERROR! Call Parameters:", call_params
            print "Std out", p

        try:
            '''
            # This allows the data to be imported if you wanted to use it
            ms_data = numpy.loadtxt(msfile, dtype='float')
            A = ms_data[:, 0]
            B = ms_data[:, 1]

            return A, B
            '''
            return None, None

        except Exception, e:
            print e
            return None, None
