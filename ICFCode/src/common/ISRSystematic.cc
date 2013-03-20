#include "ISRSystematic.hh"
#include "CommonOps.hh"
#include "EventData.hh"
#include "KinSuite.hh"
#include "TH1D.h"
#include "TH2D.h"
#include "Types.hh"
#include "mt2_bisect.hh"
#include "AlphaT.hh"
#include "Jet.hh"
#include "Math/VectorUtil.h"
#include "JetData.hh"
#include "TMath.h"
//#include "GenMatrixBin.hh"
//#include "GenObject.hh"
#include "Compute_Variable.hh"
#include "MCOps.hh"

using namespace Operation;

// -----------------------------------------------------------------------------
ISRSystematic::ISRSystematic( const Utils::ParameterSet& ps ) :

// Misc
   dirName_( ps.Get<std::string>("DirName") ),
   nMin_( ps.Get<int>("MinObjects") ),
   nMax_( ps.Get<int>("MaxObjects") ),
   bTagAlgo_( ps.Get<int>("BTagAlgo") ),
   bTagAlgoCut_( ps.Get<double>("BTagAlgoCut") ),
   minDR_( ps.Get<double>("minDR") ),
   StandardPlots_( ps.Get<bool>("StandardPlots") ),
   threshold_( ps.Get<double>("threshold") ),
   isData_(ps.Get<bool>("isData") )

   { 
   }

// -----------------------------------------------------------------------------
//
ISRSystematic::~ISRSystematic() {}

// -----------------------------------------------------------------------------
//
void ISRSystematic::Start( Event::Data& ev ) {
   initDir( ev.OutputFile(), dirName_.c_str() );
   BookHistos();
}

// -----------------------------------------------------------------------------
//
void ISRSystematic::BookHistos() {
   if ( StandardPlots_ ){ StandardPlots(); }
}

// -----------------------------------------------------------------------------
//
bool ISRSystematic::Process( Event::Data& ev ) {
   if ( StandardPlots_ ){ StandardPlots(ev); }
   return true;
}



// -----------------------------------------------------------------------------
//
void ISRSystematic::StandardPlots() {

  // book histograms

   BookHistArray(h_nEvents,
      "n_Events",
      ";;# count",
      1, 0., 1.,
      2, 0, 1, false);

   BookHistArray(h_ISRsystem_pT,
      "ISRsystem_pT",
      ";ISR system pT (GeV);# count",
      100, 0., 800.,
      1, 0, 1, false);

   BookHistArray(h_ttbarsystem_pT,
      "ttbarsystem_pT",
      ";ttbar system pT (GeV);# count",
      100, 0., 800.,
      1, 0, 1, false);

   BookHistArray(h_nJets,
      "n_Jets",
      ";nJets;# count",
      20, 0., 20.,
      1, 0, 1, true);

   BookHistArray(h_nBTagJets,
      "n_BTagged_Jets",
      ";nBJets;# count",
      10, 0., 10.,
      1, 0, 1, true);

   BookHistArray(h_LDMuon_n,
      "LDMuon_n",
      ";;# count",
      9, 0., 9.,
      1, 0, 1, false); 

   BookHistArray(h_LDMuon_pT,
      "LDMuon_pT",
      ";;# count",
      100, 0., 800.,
      1, 0, 1, false);

   BookHistArray(h_LDMuon_eta,
      "LDMuon_eta",
      ";;# count",
      50, -5., 5.,
      1, 0, 1, false);   

   BookHistArray(h_LDMuon_iso,
      "LDMuon_iso",
      ";;# count",
      100, 0., 5.,
      1, 0, 1, false);

   BookHistArray(h_LDMuon_isMuon,
      "LDMuon_isMuon",
      ";;# count",
      2, 0., 2.,
      1, 0, 1, false);   

   BookHistArray(h_LDCommonMuon_n,
      "LDCommonMuon_n",
      ";;# count",
      9, 0., 9.,
      1, 0, 1, false);

   BookHistArray(h_LDCommonMuon_pT,
      "LDCommonMuon_pT",
      ";;# count",
      100, 0., 800.,
      1, 0, 1, false);

   BookHistArray(h_LDCommonMuon_eta,
      "LDCommonMuon_eta",
      ";;# count",
      50, -5., 5.,
      1, 0, 1, false);   

   BookHistArray(h_LDCommonMuon_iso,
      "LDCommonMuon_iso",
      ";;# count",
      100, 0., 5.,
      1, 0, 1, false);

   BookHistArray(h_LDCommonMuon_isMuon,
      "LDCommonMuon_isMuon",
      ";;# count",
      2, 0., 2.,
      1, 0, 1, false);

   BookHistArray(h_LDElectron_n,
      "LDElectron_n",
      ";;# count",
      9, 0., 9.,
      1, 0, 1, false); 

   BookHistArray(h_LDElectron_pT,
      "LDElectron_pT",
      ";;# count",
      100, 0., 800.,
      1, 0, 1, false);

   BookHistArray(h_LDElectron_eta,
      "LDElectron_eta",
      ";;# count",
      50, -5., 5.,
      1, 0, 1, false);   

   BookHistArray(h_LDElectron_iso,
      "LDElectron_iso",
      ";;# count",
      100, 0., 5.,
      1, 0, 1, false);

   BookHistArray(h_LDElectron_isElectron,
      "LDElectron_isElectron",
      ";;# count",
      2, 0., 2.,
      1, 0, 1, false);   

   BookHistArray(h_LDCommonElectron_n,
      "LDCommonElectron_n",
      ";;# count",
      9, 0., 9.,
      1, 0, 1, false); 

   BookHistArray(h_LDCommonElectron_pT,
      "LDCommonElectron_pT",
      ";;# count",
      100, 0., 800.,
      1, 0, 1, false);

   BookHistArray(h_LDCommonElectron_eta,
      "LDCommonElectron_eta",
      ";;# count",
      50, -5., 5.,
      1, 0, 1, false);   

   BookHistArray(h_LDCommonElectron_iso,
      "LDCommonElectron_iso",
      ";;# count",
      100, 0., 5.,
      1, 0, 1, false);

   BookHistArray(h_LDCommonElectron_isElectron,
      "LDCommonElectron_isElectron",
      ";;# count",
      2, 0., 2.,
      1, 0, 1, false);

}



// -----------------------------------------------------------------------------
//
std::ostream& ISRSystematic::Description( std::ostream& ostrm ) {
   ostrm << "ISR Systematic selection ";
   ostrm << "(bins " << nMin_ << " to " << nMax_ << ") ";
   return ostrm;
}


// -----------------------------------------------------------------------------
//
bool ISRSystematic::StandardPlots( Event::Data& ev ) {

   unsigned int nobjkt = ev.CommonObjects().size();
   double evWeight = ev.GetEventWeight();

   //std::cout << dirName_.c_str() << " " << ev.LD_CommonMuons().accepted.size() << " " << ev.LD_Muons().size() << std::endl;
   // fill some raw muon info
   for(unsigned int l=0; l<ev.LD_Muons().size(); l++){
      h_LDMuon_pT[0]->Fill(ev.LD_Muons().at(l).Pt(), evWeight);
      h_LDMuon_eta[0]->Fill(ev.LD_Muons().at(l).Eta(), evWeight);
      h_LDMuon_iso[0]->Fill(ev.LD_Muons().at(l).GetPFIsolation(), evWeight);
      h_LDMuon_isMuon[0]->Fill(ev.muonIsGlobalMuon()->at(ev.LD_Muons().at(l).GetIndex()), evWeight);
   }
   for(unsigned int l=0; l<ev.LD_CommonMuons().accepted.size(); l++){
      h_LDCommonMuon_pT[0]->Fill(ev.LD_CommonMuons().accepted.at(l)->Pt(), evWeight);
      h_LDCommonMuon_eta[0]->Fill(ev.LD_CommonMuons().accepted.at(l)->Eta(), evWeight);
      h_LDCommonMuon_iso[0]->Fill(ev.LD_CommonMuons().accepted.at(l)->GetPFIsolation(), evWeight);
      h_LDCommonMuon_isMuon[0]->Fill(ev.muonIsGlobalMuon()->at(ev.LD_CommonMuons().accepted.at(l)->GetIndex()), evWeight);
   }
   h_LDMuon_n[0]->Fill(ev.LD_Muons().size(), evWeight);
   h_LDCommonMuon_n[0]->Fill(ev.LD_CommonMuons().accepted.size(), evWeight);

   // fill some raw electron info
   for(unsigned int l=0; l<ev.LD_Electrons().size(); l++){
      h_LDElectron_pT[0]->Fill(ev.LD_Electrons().at(l).Pt(), evWeight);
      h_LDElectron_eta[0]->Fill(ev.LD_Electrons().at(l).Eta(), evWeight);
      h_LDElectron_iso[0]->Fill(ev.LD_Electrons().at(l).GetPFIsolation(), evWeight);
   }
   for(unsigned int l=0; l<ev.LD_CommonElectrons().accepted.size(); l++){
      h_LDCommonElectron_pT[0]->Fill(ev.LD_CommonElectrons().accepted.at(l)->Pt(), evWeight);
      h_LDCommonElectron_eta[0]->Fill(ev.LD_CommonElectrons().accepted.at(l)->Eta(), evWeight);
      h_LDCommonElectron_iso[0]->Fill(ev.LD_CommonElectrons().accepted.at(l)->GetPFIsolation(), evWeight);
   }
   h_LDElectron_n[0]->Fill(ev.LD_Electrons().size(), evWeight);
   h_LDCommonElectron_n[0]->Fill(ev.LD_CommonElectrons().accepted.size(), evWeight);

   h_nEvents[0]->Fill( .5 );

   // A couple event level vetoes
   if (!StandardPlots_) return true;
   if( nobjkt < nMin_ || nobjkt > nMax_ ) return true;

   // Check leptonic event content
   if (ev.LD_CommonMuons().accepted.size()!=1) return true;
   if (ev.LD_CommonElectrons().accepted.size()!=1) return true;

   h_nEvents[1]->Fill( .5, evWeight );

   double evHT                   = ev.CommonHT();
   double hadronicAlphaT         = ev.HadronicAlphaT();
   double mht                    = ev.CommonMHT().Pt();
   int nCommJet                  = ev.JD_CommonJets().accepted.size();
   int nbjet                     = 0;
   int bIndex_0                  = 0;
   int bIndex_1                  = 0;
   vector<double> v_MHTMET       = getMHTandMET( ev );
   //vector<double> v_StopGenPt    = getStopGenPt( ev );


   for(int i=0; i<nCommJet; i++){
      
      // Count number of btagged jets
      if( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), bTagAlgo_) > bTagAlgoCut_ ) nbjet++;
      
      // Note the hardest two bjets indices
      if (nbjet==1) bIndex_0 = i;
      if (nbjet==2) bIndex_1 = i;

   }

   h_nBTagJets[0] ->Fill(nbjet, evWeight);
   h_nJets[0]     ->Fill(nCommJet, evWeight);

   // Calculate ISR system jetPt
   double isrJetPt = 0.;

   for(int i=0; i<nCommJet; i++){

      // Veto the bjets
      if ( (i==bIndex_0) || (i==bIndex_1) ) continue;
   
      isrJetPt += ev.JD_CommonJets().accepted.at(i)->Pt();

   }

   if (isrJetPt>0.) h_ISRsystem_pT[0]->Fill(isrJetPt, evWeight);

   // Calculate ttbar system Pt for shiggles
   double ttbarPt = 0.;
   ttbarPt += ev.LD_CommonMuons().accepted.at(0)->Pt();
   ttbarPt += ev.LD_CommonElectrons().accepted.at(0)->Pt();
   ttbarPt += ev.JD_CommonJets().accepted.at(bIndex_0)->Pt();
   ttbarPt += ev.JD_CommonJets().accepted.at(bIndex_1)->Pt();

   h_ttbarsystem_pT[0]->Fill( ttbarPt, evWeight );

   return true;

}


// -----------------------------------------------------------------------------
//
vector<double> ISRSystematic::getMHTandMET( Event::Data& ev ){

  vector<double> rev;

  PolarLorentzV mHT(0.,0.,0.,0.);
  std::vector<Event::Jet const *>::const_iterator ijet = ev.JD_CommonJets().accepted.begin();
  std::vector<Event::Jet const *>::const_iterator jjet = ev.JD_CommonJets().accepted.end();
  std::vector<Event::Jet const *>::const_iterator ibaby = ev.JD_CommonJets().baby.begin();
  std::vector<Event::Jet const *>::const_iterator jbaby = ev.JD_CommonJets().baby.end();

  for(; ijet!=jjet; ++ijet){
    if( (*ijet)->Pt() > threshold_ ){
      mHT -= (**ijet);
    }
  }
  for( ; ibaby!=jbaby; ++ibaby){
    if( (*ibaby)->pt() > threshold_ ){
      mHT -= (**ibaby);
    }
  }

  rev.push_back(mHT.Pt());
  LorentzV calomet = LorentzV(*ev.metP4pfTypeI());
  //  LorentzV calomet = LorentzV(*ev.metP4ak5());
  //  LorentzV calomet = LorentzV(*ev.metP4calo());
  //  LorentzV calomet = LorentzV(*ev.metP4pf());
  //  LorentzV calomet = LorentzV(*ev.metP4caloTypeI());

  for(int i = 0; i < int(ev.LD_CommonElectrons().accepted.size());i++){
    calomet = calomet+(*ev.LD_CommonElectrons().accepted[i]);
  }
  for(int i = 0; i < int(ev.PD_CommonPhotons().accepted.size());i++){
    calomet = calomet+(*ev.PD_CommonPhotons().accepted[i]);
  }
  for(int i = 0; i < int(ev.LD_CommonMuons().accepted.size());i++){
    calomet = calomet+(*ev.LD_CommonMuons().accepted[i]);
  }

  rev.push_back(calomet.Pt());

  double mhtovermet = mHT.Pt()/calomet.Pt();
  rev.push_back( mhtovermet );

  return rev;

}


// -----------------------------------------------------------------------------
//
//vector<double> ISRSystematic::getStopGenPt( Event::Data& ev ){
//
//   vector<double> v_genPtVals;
//
//   PolarLorentzV genPtVect(0.,0.,0.,0.);
//   double genPtScal = 0;
//
//   for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ) {
//      if ( fabs((*igen).GetID())==1000006 ){
//         genPtVect += (*igen);
//         genPtScal += (*igen).Pt();
//      }
//   }
//
//   v_genPtVals.push_back( genPtVect.Pt() );
//   v_genPtVals.push_back( genPtScal );
//
//   return v_genPtVals;
//
//}
