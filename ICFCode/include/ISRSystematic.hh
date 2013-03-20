#ifndef hadronic_include_ISRSystematic_hh
#define hadronic_include_ISRSystematicatic_hh

#include "PlottingBase.hh"
#include "Utils.hh"
#include "Types.hh"
#include "JetData.hh"
#include "EventData.hh"
//#include "GenObject.hh"
#include "Lepton.hh"

class TH1D;
class TH2D;

namespace Operation {

  class ISRSystematic : public PlottingBase {

    public:
  
      ISRSystematic( const Utils::ParameterSet& );
      ~ISRSystematic();
  
      void Start( Event::Data& );
      bool Process( Event::Data& );
      std::ostream& Description( std::ostream& );
  
    private:
  
      void BookHistos();
      std::string dirName_;
      UInt_t nMin_;
      UInt_t nMax_;
      UInt_t bTagAlgo_;
      double bTagAlgoCut_;
      double minDR_;
      bool StandardPlots_;
      bool isData_;
      double threshold_;      
  
      void StandardPlots();
      bool StandardPlots( Event::Data& ev );
      vector<double> getMHTandMET( Event::Data& ev );
      //vector<double> getStopGenPt( Event::Data& ev );
  
      //histos
      std::vector<TH1D*>  h_nEvents;
      std::vector<TH1D*>  h_ISRsystem_pT;
      std::vector<TH1D*>  h_ttbarsystem_pT;
      std::vector<TH1D*>  h_nJets;
      std::vector<TH1D*>  h_nBTagJets;

      std::vector<TH1D*>  h_LDMuon_n;
      std::vector<TH1D*>  h_LDMuon_pT;
      std::vector<TH1D*>  h_LDMuon_eta;
      std::vector<TH1D*>  h_LDMuon_iso;
      std::vector<TH1D*>  h_LDMuon_isMuon;

      std::vector<TH1D*>  h_LDCommonMuon_n;
      std::vector<TH1D*>  h_LDCommonMuon_pT;
      std::vector<TH1D*>  h_LDCommonMuon_eta;
      std::vector<TH1D*>  h_LDCommonMuon_iso;
      std::vector<TH1D*>  h_LDCommonMuon_isMuon;

      std::vector<TH1D*>  h_LDElectron_n;
      std::vector<TH1D*>  h_LDElectron_pT;
      std::vector<TH1D*>  h_LDElectron_eta;
      std::vector<TH1D*>  h_LDElectron_iso;
      std::vector<TH1D*>  h_LDElectron_isElectron;

      std::vector<TH1D*>  h_LDCommonElectron_n;
      std::vector<TH1D*>  h_LDCommonElectron_pT;
      std::vector<TH1D*>  h_LDCommonElectron_eta;
      std::vector<TH1D*>  h_LDCommonElectron_iso;
      std::vector<TH1D*>  h_LDCommonElectron_isElectron;

  };

}

#endif // hadronic_include_ISRSystematic_hh
