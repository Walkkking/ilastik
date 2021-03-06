import os
import tempfile
import shutil

import numpy
import vigra

from lazyflow.graph import Graph
from lazyflow.roi import roiToSlice
from lazyflow.operators.ioOperators import OpInputDataReader

from ilastik.applets.dataExport.opDataExport import OpDataExport

class TestOpDataExport(object):
    
    @classmethod
    def setupClass(cls):
        cls._tmpdir = tempfile.mkdtemp()

    @classmethod
    def teardownClass(cls):
        shutil.rmtree(cls._tmpdir) 

    def testBasic(self):
        graph = Graph()
        opExport = OpDataExport(graph=graph)
        opExport.TransactionSlot.setValue(True)        
        opExport.WorkingDirectory.setValue( self._tmpdir )
        
        # Simulate the important fields of a DatasetInfo object
        class MockDatasetInfo(object): pass
        rawInfo = MockDatasetInfo()
        rawInfo.nickname = 'test_nickname'
        rawInfo.filePath = './somefile.h5'
        opExport.RawDatasetInfo.setValue( rawInfo )

        data = numpy.random.random( (100,100) ).astype( numpy.float32 ) * 100
        data = vigra.taggedView( data, vigra.defaultAxistags('xy') )
        opExport.Input.setValue(data)

        sub_roi = [(10, 20), (90, 80)]
        opExport.RegionStart.setValue( sub_roi[0] )
        opExport.RegionStop.setValue( sub_roi[1] )
        
        opExport.ExportDtype.setValue( numpy.uint8 )
        
        opExport.OutputFormat.setValue( 'hdf5' )
        opExport.OutputFilenameFormat.setValue( '{dataset_dir}/{nickname}_export_x{x_start}-{x_stop}_y{y_start}-{y_stop}' )
        opExport.OutputInternalPath.setValue('volume/data')

        assert opExport.ImageToExport.ready()
        assert opExport.ExportPath.ready()
        
        #print "exporting data to: {}".format( opExport.ExportPath.value )
        assert opExport.ExportPath.value == self._tmpdir + '/' + rawInfo.nickname + '_export_x10-90_y20-80.h5/volume/data'
        opExport.run_export()
        
        opRead = OpInputDataReader( graph=graph )
        opRead.FilePath.setValue( opExport.ExportPath.value )

        # Compare with the correct subregion and convert dtype.
        expected_data = data.view(numpy.ndarray)[roiToSlice(*sub_roi)]
        expected_data = expected_data.astype(numpy.uint8)
        read_data = opRead.Output[:].wait()
        assert (read_data == expected_data).all(), "Read data didn't match exported data!"

if __name__ == "__main__":
    import sys
    import nose
    sys.argv.append("--nocapture")    # Don't steal stdout.  Show it on the console as usual.
    sys.argv.append("--nologcapture") # Don't set the logging level to DEBUG.  Leave it alone.
    nose.run(defaultTest=__file__)
        