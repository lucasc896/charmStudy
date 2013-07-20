#include "analysisPlots.hh"
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
#include "GenMatrixBin.hh"
#include "GenObject.hh"
#include "Compute_Variable.hh"
#include "MCOps.hh"

using namespace Operation;

// -----------------------------------------------------------------------------
analysisPlots::analysisPlots( const Utils::ParameterSet& ps ) :
// Misc
   dirName_( ps.Get<std::string>("DirName") ),
   nMin_( ps.Get<int>("MinObjects") ),
   nMax_( ps.Get<int>("MaxObjects") ),
   isData_( ps.Get<bool>("isData") ),
   bTagAlgo_( ps.Get<int>("BTagAlgo") ),
   bTagAlgoCut_( ps.Get<double>("BTagAlgoCut") ),
   minDR_( ps.Get<double>("minDR") ),
   StandardPlots_( ps.Get<bool>("StandardPlots") ),
   threshold_( ps.Get<double>("threshold") ),
   NoCuts_( ps.Get<bool>("NoCutsMode") ),
   Debug_( ps.Get<bool>("Debug") )
   
   { 
   }

// -----------------------------------------------------------------------------
//
analysisPlots::~analysisPlots() {}

// -----------------------------------------------------------------------------
//
void analysisPlots::Start( Event::Data& ev ) {
   initDir( ev.OutputFile(), dirName_.c_str() );
   BookHistos();
}

// -----------------------------------------------------------------------------
//
void analysisPlots::BookHistos() {
   if ( StandardPlots_ ){ StandardPlots(); }

}

// -----------------------------------------------------------------------------
//
bool analysisPlots::Process( Event::Data& ev ) {
   if ( StandardPlots_ ){ StandardPlots(ev); }
   return true;
}



// -----------------------------------------------------------------------------
//
void analysisPlots::StandardPlots() {

   BookHistArray(h_nEvents,
      "n_Events",
      ";;# count",
      1, 0., 1.,
      2, 0, 1, false);

   BookHistArray(h_evWeight,
      "n_evWeight",
      ";;# count",
      50, 0., 100.,
      1, 0, 1, false);

   BookHistArray(h_nJets,
      "n_Jets",
      ";nJets;# count",
      10, 0., 10.,
      1, 0, 1, true);       

   BookHistArray(h_nBTagJets,
      "n_BTagged_Jets",
      ";nBJets;# count",
      10, 0., 10.,
      7, 0, 1, true);

   BookHistArray(h_jetPt,
      "jetPt",
      ";jet p_{T} (GeV);# count",
      80, 0., 1000.,
      6, 0, 1, false);   

   BookHistArray(h_leadJetPt,
      "leadJetPt",
      ";lead jet p_{T} (GeV);# count",
      80, 0., 1000.,
      6, 0, 1, false);

   BookHistArray(h_subLeadJetPt,
      "subLeadJetPt",
      ";sublead jet p_{T} (GeV);# count",
      80, 0., 1000.,
      6, 0, 1, false);   

   BookHistArray(h_thirdJetPt,
      "thirdJetPt",
      ";third jet p_{T} (GeV);# count",
      80, 0., 1000.,
      6, 0, 1, false);

   BookHistArray(h_fourthJetPt,
      "fourthJetPt",
      ";fourth jet p_{T} (GeV);# count",
      80, 0., 1000.,
      6, 0, 1, false);   

   BookHistArray(h_fivePlusJetPt,
      "fivePlusJetPt",
      ";fivePlus jet p_{T} (GeV);# count",
      80, 0., 1000.,
      6, 0, 1, false);  

   BookHistArray(h_commHT,
      "commHT",
      ";HT (GeV);# count",
      75, 0., 1500.,
      6, 0, 1, false);

   BookHistArray(h_MET,
      "MET",
      ";MET (GeV);# count",
      50, 0., 1000.,
      6, 0, 1, false);

   BookHistArray(h_MHT,
      "MHT",
      ";MHT (GeV);# count",
      50, 0., 1000.,
      6, 0, 1, false);

   BookHistArray(h_MHToverMET,
      "MHToverMET",
      ";MHT/MET;# count",
      40, 0., 4.,
      6, 0, 1, false);     

   BookHistArray(h_MHToverHT,
      "MHToverHT",
      ";MHT/HT;# count",
      15, 0., 1.5,
      6, 0, 1, false);  

   BookHistArray(h_hadronicAlphaTZoom,
      "hadronicAlphaTZoom",
      ";alphaT;# count",
      50, 0., 1.5,
      6, 0, 1, false);

   BookHistArray(h_genPartonHT,
      "genPartonHT",
      ";Gen Parton H_T;# count",
      300, 0., 1500.,
      6, 0, 1, false);

   BookHistArray(h_leadJetdelPhi,
      "leadJetdelPhi",
      ";#delta #phi (lead two jets);# count",
      50, 0., 3.2,
      6, 0, 1, false);

   BookHistArray(h_charmJetPt_0,
      "charmJetPt_0",
      ";lead charm p_{T} (GeV);# count",
      150, 0., 800.,
      6, 0, 1, false); 

   BookHistArray(h_charmJetPt_1,
      "charmJetPt_1",
      ";sublead charm p_{T} (GeV);# count",
      64, 0., 800.,
      6, 0, 1, false); 

   BookHistArray(h_stopGenPtVect,
      "stopGenPtVect",
      ";vectorial gen p_{T};# count",
      100, 0., 1000.,
      6, 0, 1, false);

   BookHistArray(h_stopGenPtScal,
      "stopGenPtScal",
      ";scalar gen p_{T};# count",
      100, 0., 1000.,
      6, 0, 1, false);

   BookHistArray(h_dPhiStopCharm,
      "dPhiStopCharm",
      ";#delta #phi (stop-charm);# count",
      25, 0, 3.2,
      6, 0, 1, false);

   BookHistArray(h_dPhiNeutCharm,
      "dPhiNeutCharm",
      ";#delta #phi (neut-charm);# count",
      25, 0, 3.2,
      6, 0, 1, false);

   BookHistArray(h_dPhiStopNeut,
      "dPhiStopNeut",
      ";#delta #phi (stop-neut);# count",
      25, 0, 3.2,
      6, 0, 1, false);

   BookHistArray(h_dPhiStopStop,
      "dPhiStopStop",
      ";#delta #phi (stop-stop);# count",
      25, 0, 3.2,
      6, 0, 1, false);

   BookHistArray(h_dPhiCharmCharm,
      "dPhiCharmCharm",
      ";#delta #phi (charm-charm);# count",
      25, 0, 3.2,
      6, 0, 1, false);   

   BookHistArray(h_dPhiLeadJetMHT,
      "dPhiLeadJetMHT",
      ";#delta #phi (leadJet-MHT);# count",
      25, 0, 3.2,
      6, 0, 1, false); 

   BookHistArray(h_dPhiSubLeadJetMHT,
      "dPhiSubLeadJetMHT",
      ";#delta #phi (subLeadJet-MHT);# count",
      25, 0, 3.2,
      6, 0, 1, false); 

   BookHistArray(h_susyScanPlane,
      "susyScanPlane",
      ";mSQ (GeV); mLSP (GeV)",
      80, 0., 400., 
      80, 0., 400.,
      6, 0, 1, false); 

   BookHistArray(h_alphaT_vs_HT,
   "alphaT_vs_HT",
   ";HT (GeV);alphaT",
   140, 175., 875.,
   250,0.5, 3.,
   6, 0, 1, false);

   BookHistArray(h_vectGenPt_vs_scalGenPt,
      "vectGenPt_vs_scalGenPt",
      ";vectorial gen p_{T} stop pair (GeV);scalar gen p_T stop pair (GeV);",
      64, 0., 1000.,
      64, 0., 1000.,
      1, 0, 1, false);

   BookHistArray(h_leadTwoJetsPt,
      "leadTwoJetsPt",
      ";two lead jets p_{T} (GeV);# count",
      80 , 0., 1000.,
      6, 0, 1, false);

   BookHistArray(h_nVertex,
      "nVertex",
      ";nVertices;# count",
      40, 0., 40.,
      6, 0, 1, false);

   BookHistArray(h_nIsoTrack,
      "nIsoTrack",
      ";nIsoTrack;# count",
      10, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_pfCandsPtDiff,
      "pfCandsPtDiff",
      ";P4.Pt() - Pt;# count",
      100, -20., 20.,
      2, 0, 1, false);

   BookHistArray(h_pfCandsPt,
      "pfCandsPt",
      ";Pt;# count",
      100, 0., 100.,
      2, 0, 1, false);

   BookHistArray(h_pfCandsEta,
      "pfCandsEta",
      ";Eta;# count",
      100, -3., 3.,
      2, 0, 1, false);

   BookHistArray(h_pfCandsDzPV,
      "pfCandsDzPV",
      ";Pt;# count",
      100, 0., 2.,
      2, 0, 1, false);

   BookHistArray(h_pfCandsDunno,
      "pfCandsDunno",
      ";Pt;# count",
      100, 0., 10.,
      2, 0, 1, false);

}


// -----------------------------------------------------------------------------
//
std::ostream& analysisPlots::Description( std::ostream& ostrm ) {
   ostrm << "Charm Study Analysis Plots ";
   ostrm << "(bins " << nMin_ << " to " << nMax_ << ") ";
   return ostrm;
}


// -----------------------------------------------------------------------------
// Main module
bool analysisPlots::StandardPlots( Event::Data& ev ) {
   
   // double start_time = omp_get_wtime();

   unsigned int nobjkt = ev.CommonObjects().size();
   double evWeight = ev.GetEventWeight();

   h_evWeight[0]->Fill(evWeight);
   h_nEvents[0]->Fill( .5 );

   // a couple event level vetoes
   if (!StandardPlots_) return true;
   if (!NoCuts_){
      if( nobjkt < nMin_ || nobjkt > nMax_ ) return true;
   }

   h_nEvents[1]->Fill( .5, evWeight );

   // fill some isoTrack variables
   int j=0;
   for(unsigned int i=0; i<ev.pfCandsPt()->size(); i++){
      
      // simulate 5GeV pt cut form SusyCAF
      if (ev.pfCandsPt()->at(i) < 5.) continue;
      
      // stop out of range access
      if (j>=ev.pfCandsP4()->size()) break;

      h_pfCandsPt[0]->Fill(ev.pfCandsPt()->at(i), evWeight);
      h_pfCandsEta[0]->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);
      h_pfCandsDzPV[0]->Fill(ev.pfCandsDzPV()->at(i), evWeight);
      h_pfCandsDunno[0]->Fill((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)), evWeight);

      if ((ev.pfCandsPt()->at(i) > 10.) &&
         (ev.pfCandsP4()->at(j).Eta() < 2.2) &&
         (ev.pfCandsDzPV()->at(i) < 0.05)){
         if ((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i))>0.1){
            // std::cout << "Veto hasn't worked..." << std::endl;
            // std::cout << ev.pfCandsPt()->at(i) << " " << ev.pfCandsP4()->at(j).Eta() << " " << ev.pfCandsDzPV()->at(i) << " " << (ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)) << std::endl;
            h_pfCandsPt[1]->Fill(ev.pfCandsPt()->at(i), evWeight);
            h_pfCandsEta[1]->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);
            h_pfCandsDzPV[1]->Fill(ev.pfCandsDzPV()->at(i), evWeight);
            h_pfCandsDunno[1]->Fill((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)), evWeight);
         }
      }
   }

   if(Debug_) std::cout << "generic event variables" << std::endl;
   // get generic event variables
   double evHT             = ev.CommonHT();
   double hadronicAlphaT   = ev.HadronicAlphaT();
   double mht              = ev.CommonMHT().Pt();
   int nCommJet            = ev.JD_CommonJets().accepted.size();
   vector<double> v_MHTMET = getMHTandMET( ev );
   int nbjet = 0;
   vector<double> v_StopGenPt;

   if (!isData_) v_StopGenPt = getStopGenPt( ev );

   for(auto jet: ev.JD_CommonJets().accepted){
      // count number of btagged jets
      if( ev.GetBTagResponse(jet->GetIndex(), bTagAlgo_) > bTagAlgoCut_ ) nbjet++;
   }

   h_nJets[0]     ->Fill( nCommJet, evWeight );
   h_nBTagJets[0] ->Fill( nbjet, evWeight );

   // get nVertices
   if(Debug_) std::cout << "nvertices" << std::endl;
   int nVertex = verticesN( ev );
   int plotIndex              = (nbjet>4) ? 5 : nbjet;

   h_nVertex[plotIndex]    ->Fill( nVertex, evWeight );
   h_nIsoTrack[plotIndex]  ->Fill( getNIsoTrack( ev ), evWeight );

   for(auto jet: ev.JD_CommonJets().accepted){
      h_jetPt[plotIndex]         ->Fill( jet->Pt(), evWeight );
      // h_jetPt_vs_nVtx[plotIndex] ->Fill( jet->Pt(), nVertex, evWeight );
   }

   h_nBTagJets[plotIndex+1]            ->Fill( nbjet );
   h_commHT[plotIndex]                 ->Fill( evHT, evWeight );
   // h_commHT_vs_nVtx[plotIndex]         ->Fill( evHT, nVertex, evWeight );
   h_hadronicAlphaTZoom[plotIndex]     ->Fill( hadronicAlphaT, evWeight );
   h_MHT[plotIndex]                    ->Fill( mht, evWeight );
   // h_MHT_vs_nVtx[plotIndex]            ->Fill( mht, nVertex, evWeight);
   h_MET[plotIndex]                    ->Fill( v_MHTMET[1], evWeight );
   h_MHToverMET[plotIndex]             ->Fill( v_MHTMET[2], evWeight );
   h_alphaT_vs_HT[plotIndex]           ->Fill( evHT, hadronicAlphaT, evWeight );
   h_MHToverHT[plotIndex]              ->Fill( mht/evHT, evWeight );

   if (!isData_){
      h_stopGenPtVect[plotIndex]          ->Fill( v_StopGenPt.at(0), evWeight );
      h_stopGenPtScal[plotIndex]          ->Fill( v_StopGenPt.at(1), evWeight );
      h_vectGenPt_vs_scalGenPt[0]         ->Fill( v_StopGenPt.at(0), v_StopGenPt.at(1), evWeight );
   }

   if(Debug_) std::cout << "Pre jet filling" << std::endl;

   double leadJetMHTdPhi = 0.;
   if (ev.JD_CommonJets().accepted.size()>0){
      leadJetMHTdPhi = ROOT::Math::VectorUtil::DeltaPhi( *ev.JD_CommonJets().accepted.at(0),ev.CommonMHT() );
   }

   double subLeadJetMHTdPhi = 0.;
   if (ev.JD_CommonJets().accepted.size()>1){
      subLeadJetMHTdPhi = ROOT::Math::VectorUtil::DeltaPhi( *ev.JD_CommonJets().accepted.at(1),ev.CommonMHT() );
   }   

   if (ev.JD_CommonJets().accepted.size()>0){
     h_leadJetPt[plotIndex]     ->Fill( ev.JD_CommonJets().accepted.at(0)->Pt(), evWeight );
   }

   double jetDeltaPhi = 0.;
   if (ev.JD_CommonJets().accepted.size()>1){
      jetDeltaPhi = ROOT::Math::VectorUtil::DeltaPhi(*ev.JD_CommonJets().accepted.at(0),*ev.JD_CommonJets().accepted.at(1));
      h_leadJetdelPhi[plotIndex] ->Fill( fabs(jetDeltaPhi), evWeight );
      //h_delPhi_vs_scalGenPt[0]   ->Fill( v_StopGenPt.at(1), fabs(jetDeltaPhi), evWeight );
      //h_delPhi_vs_vectGenPt[0]   ->Fill( v_StopGenPt.at(0), fabs(jetDeltaPhi), evWeight );
      
      
      h_subLeadJetPt[plotIndex]  ->Fill( ev.JD_CommonJets().accepted.at(1)->Pt(), evWeight );

      //h_leadJetPt_vs_HT[plotIndex]->Fill( ev.JD_CommonJets().accepted.at(0)->Pt(), evHT, evWeight);

      h_leadTwoJetsPt[plotIndex]->Fill( ev.JD_CommonJets().accepted.at(0)->Pt()+ev.JD_CommonJets().accepted.at(1)->Pt(), evWeight );

      //double jetDiff = ev.JD_CommonJets().accepted.at(0)->Pt() - ev.JD_CommonJets().accepted.at(1)->Pt();
      //h_leadminsubJetPt_vs_HT[plotIndex]->Fill( jetDiff, evHT, evWeight );
   }

   h_dPhiLeadJetMHT[plotIndex]->Fill( leadJetMHTdPhi, evWeight );
   h_dPhiSubLeadJetMHT[plotIndex]->Fill( subLeadJetMHTdPhi, evWeight );

   if (ev.JD_CommonJets().accepted.size()>2) h_thirdJetPt[plotIndex]->Fill(ev.JD_CommonJets().accepted.at(2)->Pt(), evWeight);
   if (ev.JD_CommonJets().accepted.size()>3) h_fourthJetPt[plotIndex]->Fill(ev.JD_CommonJets().accepted.at(3)->Pt(), evWeight);

   for(unsigned int i=0; i<ev.JD_CommonJets().accepted.size(); i++){
      if (i>3) h_fivePlusJetPt[plotIndex]->Fill(ev.JD_CommonJets().accepted.at(i)->Pt(), evWeight);
   }

   if (!isData_){
      if(Debug_) std::cout << "!isData_" << std::endl;

      // do some gen matching
      Event::GenObject *gStop1=NULL;
      Event::GenObject *gStop2=NULL;
      Event::GenObject *gCharm1=NULL;
      Event::GenObject *gCharm2=NULL;
      Event::GenObject *gNeut1=NULL;
      Event::GenObject *gNeut2=NULL;

      for(auto igen: ev.GenParticles()){
         if( igen.GetStatus() == 3 ){
            if( igen.GetID() == 1000006 )                                              gStop1   = &igen; 
            if( igen.GetID() == -1000006 )                                             gStop2   = &igen; 
            if( (fabs(igen.GetID()) == 4) && (igen.GetMotherID() == 1000006) )         gCharm1  = &igen;
            if( (fabs(igen.GetID()) == 4) && (igen.GetMotherID() == -1000006) )        gCharm2  = &igen;
            if( (fabs(igen.GetID()) == 1000022) && (igen.GetMotherID() == 1000006) )   gNeut1   = &igen; 
            if( (fabs(igen.GetID()) == 1000022) && (igen.GetMotherID() == -1000006) )  gNeut2   = &igen; 
         }

      }

      // fill gen-level dPhi distros
      if( gStop1 && gStop2 && gCharm1 && gCharm2 && gNeut1 && gNeut2 ){
         h_dPhiStopCharm[plotIndex]  ->Fill( getGenDeltaPhi(*gStop1, *gCharm1), evWeight );
         h_dPhiStopCharm[plotIndex]  ->Fill( getGenDeltaPhi(*gStop2, *gCharm2), evWeight );
         h_dPhiNeutCharm[plotIndex]  ->Fill( getGenDeltaPhi(*gNeut1, *gCharm1), evWeight );
         h_dPhiNeutCharm[plotIndex]  ->Fill( getGenDeltaPhi(*gNeut2, *gCharm2), evWeight );
         h_dPhiStopNeut[plotIndex]   ->Fill( getGenDeltaPhi(*gStop1, *gNeut1), evWeight );
         h_dPhiStopNeut[plotIndex]   ->Fill( getGenDeltaPhi(*gStop2, *gNeut2), evWeight );
         h_dPhiStopStop[plotIndex]   ->Fill( getGenDeltaPhi(*gStop1, *gStop2), evWeight );
         h_dPhiCharmCharm[plotIndex] ->Fill( getGenDeltaPhi(*gCharm1, *gCharm2), evWeight );
      }

      // get out SMS variables
      double M0 = 0.;
      double M12 = 0.;

      if(ev.M0.enabled())     M0 = ev.M0();
      if(ev.MG.enabled())     M0 = ev.MG();
      if(ev.MLSP.enabled())   M12 = ev.MLSP();
      if(ev.M12.enabled())    M12 = ev.M12();

      h_susyScanPlane[plotIndex]->Fill( M0, M12, evWeight );

      // h_SMSscalGenPt[0]->Fill( M0, M12, v_StopGenPt.at(1*evWeight) );
      // h_SMSvectGenPt[0]->Fill( M0, M12, v_StopGenPt.at(0)*evWeight );
      // h_SMSdPhiLeadJetsGenPt[0]->Fill( M0, M12, jetDeltaPhi*evWeight );
      // h_SMSAlphaT[0]   ->Fill( M0, M12, hadronicAlphaT*evWeight );

      h_genPartonHT[plotIndex]->Fill( ev.GetPartonHT(), evWeight );


   } // !isData_

   return true;

}


// -----------------------------------------------------------------------------
// Module to calculate the correct histogram index according to btagging
int analysisPlots::getPlotIndex( int nbjet ){

   for(int i=0; i<5; i++){
      if (nbjet==i)  return i;
      if (nbjet>4)   return 5;
   }

   return 0;

}


// -----------------------------------------------------------------------------
// Module to get MHT and MET
vector<double> analysisPlots::getMHTandMET( Event::Data& ev ){

  vector<double> rev;

  PolarLorentzV mHT(0.,0.,0.,0.);
  // std::vector<Event::Jet const *>::const_iterator ijet = ev.JD_CommonJets().accepted.begin();
  // std::vector<Event::Jet const *>::const_iterator jjet = ev.JD_CommonJets().accepted.end();
  // std::vector<Event::Jet const *>::const_iterator ibaby = ev.JD_CommonJets().baby.begin();
  // std::vector<Event::Jet const *>::const_iterator jbaby = ev.JD_CommonJets().baby.end();

  for(auto ijet: ev.JD_CommonJets().accepted){
    if( ijet->Pt() > threshold_ ){
      mHT -= *ijet;
    }
  }
  for(auto ibaby: ev.JD_CommonJets().baby){
    if( ibaby->pt() > threshold_ ){
      mHT -= *ibaby;
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
// Module to get the genLevel scalar and vector sumPt of the stop pair
vector<double> analysisPlots::getStopGenPt( Event::Data& ev ){

   vector<double> v_genPtVals;

   PolarLorentzV genPtVect(0.,0.,0.,0.);
   double genPtScal = 0;

   for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ) {
      if ( fabs((*igen).GetID())==1000006 ){
         genPtVect += (*igen);
         genPtScal += (*igen).Pt();
      }
   }

   v_genPtVals.push_back( genPtVect.Pt() );
   v_genPtVals.push_back( genPtScal );

   return v_genPtVals;

}


// -----------------------------------------------------------------------------
// Module to get the deltaPhi between two genLevel objects
double analysisPlots::getGenDeltaPhi( const Event::GenObject& gOb1, const Event::GenObject& gOb2 ){

   double dPhi = ROOT::Math::VectorUtil::DeltaPhi( gOb1, gOb2 );
   return fabs( dPhi );

}


// -----------------------------------------------------------------------------
// Module to get number of vertices passing quality cuts - from Z. Meng
int analysisPlots::verticesN( Event::Data& ev ){
  int nVertex=0;
  for(std::vector<float>::const_iterator vtx= ev.vertexSumPt()->begin();vtx != ev.vertexSumPt()->end();++vtx){
    if(!ev.vertexIsFake()->at( vtx-ev.vertexSumPt()->begin()) &&
       fabs((ev.vertexPosition()->at( vtx-ev.vertexSumPt()->begin())).Z()) < 24.0 &&
       ev.vertexNdof()->at( vtx-ev.vertexSumPt()->begin() ) > 4 &&
       (ev.vertexPosition()->at( vtx-ev.vertexSumPt()->begin())).Rho() < 2.0 ){
      nVertex++;
    }
  }
  return nVertex;
}


// -----------------------------------------------------------------------------
// Module to get the number of isolated tracks (connected to SITV)
int analysisPlots::getNIsoTrack( Event::Data& ev ){
       
   // if one branch isn't enabled, return true - no pfCands in event
   if (!ev.pfCandsPt.enabled()) return 0;

   /*
    Note: double loop is used due to bad placement of 5GeV pT cut in SusyCAF code.
    P4 and Pt vectors are different lengths.
   */

   int nIso = 0;
   // loop over all pfCands
   
   int j=0;
   for(unsigned int i=0; i<ev.pfCandsPt()->size(); i++){

      // simulate 5GeV pt cut form SusyCAF
      if (ev.pfCandsPt()->at(i) < 5.) continue;
      // stop out of range access
      if (j>=ev.pfCandsP4()->size()) break;
      // return false if any candidate meets isoTrack reqs
      if ((ev.pfCandsPt()->at(i) > 10.) &&
         // (ev.pfCandsP4()->at(j).Eta() < mMaxEta_) &&
         (ev.pfCandsCharge()->at(i) != 0) &&
         (ev.pfCandsDzPV()->at(i) < 0.05)){
            if ((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)) < 0.1){
               nIso++;
            }
      }
      j++;
   } //pfCands for loop

    return nIso;
}
