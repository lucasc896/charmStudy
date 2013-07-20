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
      const Event::GenObject* getGenITMatch( Event::Data& ev, fourMomenta p4IT );
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

      // Histos
      std::vector<TH1D*>  h_nEvents;
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

      std::vector<TH1D*>  h_GenEleN;
      std::vector<TH1D*>  h_GenMuN;
      std::vector<TH1D*>  h_GenTauHadN;
      std::vector<TH1D*>  h_GenOtherN;
      std::vector<TH1D*>  h_GenEleNoMatchN;
      std::vector<TH1D*>  h_GenMuNoMatchN;
      std::vector<TH1D*>  h_GenTauHadNoMatchN;
      std::vector<TH1D*>  h_GenOtherNoMatchN;

      std::vector<TH1D*>  h_ITGenEleN;
      std::vector<TH1D*>  h_ITGenElePt;
      std::vector<TH1D*>  h_ITGenEleEta;
      std::vector<TH1D*>  h_ITGenMuN;
      std::vector<TH1D*>  h_ITGenMuPt;
      std::vector<TH1D*>  h_ITGenMuEta;
      std::vector<TH1D*>  h_ITGenHadTauN;
      std::vector<TH1D*>  h_ITGenHadTauPt;
      std::vector<TH1D*>  h_ITGenHadTauEta;
      std::vector<TH1D*>  h_ITGenHadTauPtDiff;
      std::vector<TH1D*>  h_ITGenOtherN;
      std::vector<TH1D*>  h_ITGenOtherPt;
      std::vector<TH1D*>  h_ITGenOtherEta;
      std::vector<TH1D*>  h_ITNoMatchN;
      std::vector<TH1D*>  h_ITNoMatchPt;
      std::vector<TH1D*>  h_ITNoMatchEta;

      // std::vector<TH1D*>  h_tmpDR;
      std::vector<TH1D*>  h_matchPtDiff;

  };

}

#endif // hadronic_include_isoTrackPlots_hh
