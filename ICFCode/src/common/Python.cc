#include <boost/python.hpp>
#include "charmEffStudy.hh"
#include "analysisPlots.hh"
#include "isoTrackPlots.hh"
#include "charmFilters.hh"

using namespace boost::python;

BOOST_PYTHON_MODULE(lib_charmStudy) {

   class_<Operation::charmEffStudy, bases<Operation::_Base> >( "OP_charmEffStudy",
                     init<const Utils::ParameterSet&>() );

   class_<Operation::analysisPlots, bases<Operation::_Base> >( "OP_analysisPlots",
                     init<const Utils::ParameterSet&>() );

   class_<Operation::isoTrackPlots, bases<Operation::_Base> >( "OP_isoTrackPlots",
		     init<const Utils::ParameterSet&>() );

   class_<Operation::StopGenVectCut, bases<Operation::_Base> >( "OP_StopGenVectPtSumCut",
                     init<float>() );

}
