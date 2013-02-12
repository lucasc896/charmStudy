#include <boost/python.hpp>
#include "charmEffStudy.hh"
#include "analysisPlots.hh"
#include "ISRSystematic.hh"

using namespace boost::python;

BOOST_PYTHON_MODULE(lib_charmStudy) {

   class_<Operation::charmEffStudy, bases<Operation::_Base> >( "OP_charmEffStudy",
                     init<const Utils::ParameterSet&>());

   class_<Operation::analysisPlots, bases<Operation::_Base> >( "OP_analysisPlots",
                     init<const Utils::ParameterSet&>());

   class_<Operation::ISRSystematic, bases<Operation::_Base> >( "OP_ISRSystematic",
                     init<const Utils::ParameterSet&>());

}
