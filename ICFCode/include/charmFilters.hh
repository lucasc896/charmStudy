#ifndef hadronic_include_charmFilters_hh
#define hadronic_include_charmFilters_hh

#include "EventData.hh"
#include "Math/VectorUtil.h"
#include "Operation.hh"
#include "TH1F.h"
#include "GenMatrixBin.hh"
#include "GenObject.hh"


namespace Operation {


  class StopGenVectCut : public Operation::_Base {
  public:
    StopGenVectCut( float );
    ~StopGenVectCut() {;}
    bool Process( Event::Data& );
    std::ostream& Description( std::ostream& );
  private:
    float cut_;
  };

  // -----------------------------------------------------------------------------
  //
  StopGenVectCut::StopGenVectCut( float cut )
    : cut_(cut)
    {;}

  // -----------------------------------------------------------------------------
  //
  bool StopGenVectCut::Process( Event::Data& ev ) {
    if ( ev.CommonObjects().size() < 2 ||
      ev.CommonObjects().size() > 50 ) { return false; }

    PolarLorentzV genPtVect(0.,0.,0.,0.);

    for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ) {
      if ( fabs((*igen).GetID())==1000006 ){
         genPtVect += (*igen);
      }
    }

    if ( genPtVect.Pt() <= cut_ ) { return true; }
    return false;
  }

  // -----------------------------------------------------------------------------
  //
  std::ostream& StopGenVectCut::Description( std::ostream &ostrm ) {
    ostrm << "StopGenVectCut less than " << cut_ << " " ;
    return ostrm;
  }


}

#endif // hadronic_include_charmFilters_hh





