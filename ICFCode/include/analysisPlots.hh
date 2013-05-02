#ifndef hadronic_include_analysisPlots_hh
#define hadronic_include_analysisPlots_hh

#include "PlottingBase.hh"
#include "Utils.hh"
#include "Types.hh"
#include "JetData.hh"
#include "EventData.hh"
#include "GenObject.hh"
#include "Lepton.hh"

class TH1D;
class TH2D;

namespace Operation {

  class analysisPlots : public PlottingBase {

    public:
  
      analysisPlots( const Utils::ParameterSet& );
      ~analysisPlots();
  
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
 
      void StandardPlots();
      bool StandardPlots( Event::Data& ev );

      // User-defined modules
      int getPlotIndex( int nbjet );
      vector<double> getMHTandMET( Event::Data& ev );
      vector<double> getStopGenPt( Event::Data& ev );
      double getGenDeltaPhi( const Event::GenObject& gOb1, const Event::GenObject& gOb2 );
      int verticesN( Event::Data& ev );
  
      // Histos
      std::vector<TH1D*>  h_nEvents;
      std::vector<TH1D*>  h_evWeight;
      std::vector<TH1D*>  h_nJets;
      std::vector<TH1D*>  h_nJets_charm;
      std::vector<TH1D*>  h_nJets_ISR;
      std::vector<TH1D*>  h_nBTagJets;
      std::vector<TH1D*>  h_jetPt;
      std::vector<TH1D*>  h_charmJetPt_0;
      std::vector<TH1D*>  h_charmJetPt_1;
      std::vector<TH1D*>  h_leadJetPt;
      std::vector<TH1D*>  h_subLeadJetPt;
      std::vector<TH1D*>  h_leadISRJetPt;
      std::vector<TH1D*>  h_subLeadISRJetPt;      
      std::vector<TH1D*>  h_thirdJetPt;
      std::vector<TH1D*>  h_fourthJetPt;
      std::vector<TH1D*>  h_fivePlusJetPt;
      std::vector<TH1D*>  h_commHT;
      std::vector<TH1D*>  h_HT_charm;
      std::vector<TH1D*>  h_HT_ISR;
      std::vector<TH1D*>  h_MET;
      std::vector<TH1D*>  h_MHT;
      std::vector<TH1D*>  h_MHToverMET;
      std::vector<TH1D*>  h_MHToverHT;
      std::vector<TH1D*>  h_hadronicAlphaT;
      std::vector<TH1D*>  h_hadronicAlphaTZoom;
      std::vector<TH1D*>  h_leadJetdelPhi;
      std::vector<TH1D*>  h_stopGenPtVect;
      std::vector<TH1D*>  h_stopGenPtScal;
      //std::vector<TH2D*>  h_delPhi_vs_scalGenPt;
      //std::vector<TH2D*>  h_delPhi_vs_vectGenPt;
      std::vector<TH1D*>  h_dPhiStopCharm;
      std::vector<TH1D*>  h_dPhiNeutCharm;
      std::vector<TH1D*>  h_dPhiStopStop;
      std::vector<TH1D*>  h_dPhiCharmCharm;
      std::vector<TH1D*>  h_dPhiStopNeut;
      std::vector<TH1D*>  h_dPhiLeadJetMHT;
      std::vector<TH1D*>  h_dPhiSubLeadJetMHT;
      std::vector<TH2D*>  h_susyScanPlane;
      //std::vector<TH2D*>  h_SMSvectGenPt;
      //std::vector<TH2D*>  h_SMSscalGenPt;
      //std::vector<TH2D*>  h_SMSdPhiLeadJetsGenPt;
      //std::vector<TH2D*>  h_SMSAlphaT;
      //std::vector<TH2D*>  h_alphaT_vs_HT;
      //std::vector<TH2D*>  h_leadJetPt_vs_HT;
      //std::vector<TH2D*>  h_leadminsubJetPt_vs_HT; 
      std::vector<TH2D*>  h_vectGenPt_vs_scalGenPt;
      std::vector<TH2D*>  h_genPtLeadCharm_vs_MHT;
      std::vector<TH2D*>  h_delPhiLeadJetMHT_vs_MHT;  
      std::vector<TH1D*>  h_leadTwoJetsPt;  
      std::vector<TH2D*>  h_commHT_vs_nVtx;
      std::vector<TH2D*>  h_MHT_vs_nVtx;
      std::vector<TH2D*>  h_jetPt_vs_nVtx; 
      std::vector<TH1D*>  h_nVertex;
  };

}

#endif // hadronic_include_analysisPlots_hh
