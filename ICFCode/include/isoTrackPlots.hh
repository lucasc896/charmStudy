#ifndef hadronic_include_isoTrackPlots_hh
#define hadronic_include_isoTrackPlots_hh

#include "PlottingBase.hh"
#include "Utils.hh"
#include "Types.hh"
#include "JetData.hh"
#include "EventData.hh"
#include "GenObject.hh"
#include "Lepton.hh"

typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > fourMomenta;

class TH1D;
class TH2D;

namespace Operation {

  class isoTrackPlots : public PlottingBase {

    public:
  
      isoTrackPlots( const Utils::ParameterSet& );
      ~isoTrackPlots();
  
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
      double threshold_;      
      bool NoCuts_;
      bool isData_;
 
      void StandardPlots();
      bool StandardPlots( Event::Data& ev );

      // User-defined modules
      fourMomenta getGenITMatch( Event::Data& ev, int pID, fourMomenta p4IT );
      vector<double> getMHTandMET( Event::Data& ev );
      double getGenDeltaPhi( const Event::GenObject& gOb1, const Event::GenObject& gOb2 );
      int verticesN( Event::Data& ev );
      int getNIsoTrack( Event::Data& ev );

      bool isTrueVEle(    const Event::GenObject& gob );
      bool isTrueVMu(     const Event::GenObject& gob );
      bool isTrueEle(     const Event::GenObject& gob );
      bool isTrueMu(      const Event::GenObject& gob );
      bool isTrueTau(     const Event::GenObject& gob );
      bool isTrueZMuMu(   const Event::GenObject& gob );
      bool isTrueTauEle(  Event::Data& ev, const Event::GenObject& gob );
      bool isTrueTauMu(   Event::Data& ev, const Event::GenObject& gob );
      bool isTrueTauHad(  Event::Data& ev, const Event::GenObject& gob );
      bool isTrueTauLep(  Event::Data& ev, const Event::GenObject& gob );
      std::vector<int> theDaughterID( Event::Data * ev, int mID );

      std::vector<TH1D*>  KILL_ele;
      std::vector<TH1D*>  KILL_mu;
      std::vector<TH1D*>  ODD_ele;
      std::vector<TH1D*>  ODD_mu;

      // Histos
      std::vector<TH1D*>  h_nEvents;
      std::vector<TH1D*>  h_nEventsTauEle;
      std::vector<TH1D*>  h_nEventsTauMu;
      std::vector<TH1D*>  h_nEventsTauHad;
      std::vector<TH1D*>  h_nEventsVEle;
      std::vector<TH1D*>  h_nEventsVMu;
      std::vector<TH1D*>  h_nEventsOther;
      std::vector<TH1D*>  h_nEventsTauEleITMatched;
      std::vector<TH1D*>  h_nEventsTauMuITMatched;
      std::vector<TH1D*>  h_nEventsTauHadITMatched;
      std::vector<TH1D*>  h_nEventsVEleITMatched;
      std::vector<TH1D*>  h_nEventsVMuITMatched;
      std::vector<TH1D*>  h_nEventsOtherITMatched;

      std::vector<TH1D*>  h_evWeight;
      std::vector<TH1D*>  h_nJets;
      std::vector<TH1D*>  h_nBTagJets;
      std::vector<TH1D*>  h_commHT;
      std::vector<TH1D*>  h_nVertex;

      std::vector<TH1D*>  h_nIsoTrack;
      std::vector<TH1D*>  h_pfCandsPt;
      std::vector<TH1D*>  h_pfCandsEta;
      std::vector<TH1D*>  h_pfCandsDzPV;
      std::vector<TH1D*>  h_pfCandsDunno;
      std::vector<TH1D*>  h_pfCandsCharge;

      std::vector<TH1D*>  h_SIT_recoMu_pt;
      std::vector<TH1D*>  h_SIT_recoMu_eta;
      std::vector<TH1D*>  h_SIT_recoMu_combIso;
      std::vector<TH1D*>  h_SIT_recoMu_dR;
      std::vector<TH1D*>  h_SIT_recoEle_pt;
      std::vector<TH1D*>  h_SIT_recoEle_eta;
      std::vector<TH1D*>  h_SIT_recoEle_combIso;
      std::vector<TH1D*>  h_SIT_recoEle_dR;

      std::vector<TH1D*>  h_genElePt;
      std::vector<TH1D*>  h_genMuPt;
      std::vector<TH1D*>  h_genTauPt;
      std::vector<TH1D*>  h_delR_eleIT;
      std::vector<TH1D*>  h_delR_muIT;
      std::vector<TH1D*>  h_delR_tauIT;
      std::vector<TH1D*>  h_delR_TauEleIT;
      std::vector<TH1D*>  h_delR_TauMuIT;
      std::vector<TH1D*>  h_delR_TauHadIT;
      std::vector<TH1D*>  h_delR_VEleIT;
      std::vector<TH1D*>  h_delR_VMuIT;
      std::vector<TH1D*>  h_genPtTauEle;
      std::vector<TH1D*>  h_genPtTauMu;
      std::vector<TH1D*>  h_genPtTauHad;
      std::vector<TH1D*>  h_genPtVEle;
      std::vector<TH1D*>  h_genPtVMu;
      std::vector<TH1D*>  h_genEtaTauEle;
      std::vector<TH1D*>  h_genEtaTauMu;
      std::vector<TH1D*>  h_genEtaTauHad;
      std::vector<TH1D*>  h_genEtaVEle;
      std::vector<TH1D*>  h_genEtaVMu;


  };

}

#endif // hadronic_include_isoTrackPlots_hh
