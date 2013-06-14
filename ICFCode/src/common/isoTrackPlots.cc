#include "isoTrackPlots.hh"
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
#include <typeinfo>

using namespace Operation;

// -----------------------------------------------------------------------------
isoTrackPlots::isoTrackPlots( const Utils::ParameterSet& ps ) :
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
   NoCuts_( ps.Get<bool>("NoCutsMode") )

   { 
   }

// -----------------------------------------------------------------------------
//
isoTrackPlots::~isoTrackPlots() {}

// -----------------------------------------------------------------------------
//
void isoTrackPlots::Start( Event::Data& ev ) {
   initDir( ev.OutputFile(), dirName_.c_str() );
   BookHistos();
}

// -----------------------------------------------------------------------------
//
void isoTrackPlots::BookHistos() {
   if ( StandardPlots_ ){ StandardPlots(); }

}

// -----------------------------------------------------------------------------
//
bool isoTrackPlots::Process( Event::Data& ev ) {
   if ( StandardPlots_ ){ StandardPlots(ev); }
   return true;
}



// -----------------------------------------------------------------------------
//
void isoTrackPlots::StandardPlots() {

   BookHistArray(h_nEvents,
      "n_Events",
      ";;# count",
      1, 0., 1.,
      2, 0, 1, false);

   BookHistArray(h_nEventsTauEle,
      "n_EventsTauEle",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsTauMu,
      "n_EventsTauMu",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsTauHad,
      "n_EventsTauHad",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsVEle,
      "n_EventsVEle",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsVMu,
      "n_EventsVMu",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsOther,
      "n_EventsOther",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsTauEleITMatched,
      "n_EventsTauEleITMatched",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsTauMuITMatched,
      "n_EventsTauMuITMatched",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsTauHadITMatched,
      "n_EventsTauHadITMatched",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsVEleITMatched,
      "n_EventsVEleITMatched",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsVMuITMatched,
      "n_EventsVMuITMatched",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_nEventsOtherITMatched,
      "n_EventsOtherITMatched",
      ";;# count",
      1, 0., 1.,
      6, 0, 1, false);   

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

   BookHistArray(h_commHT,
      "commHT",
      ";HT (GeV);# count",
      50, 0., 1000.,
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

   BookHistArray(h_pfCandsCharge,
      "pfCandsCharge",
      ";pfCands charge;# count",
      3, -1., 2.,
      1, 0, 1, false);

   BookHistArray(h_SIT_recoMu_pt,
      "h_SIT_recoMu_pt",
      ";SIT matched recoMuon pT;# count",
      100, 0., 100.,
      6, 0, 1, false);

   BookHistArray(h_SIT_recoMu_eta,
      "h_SIT_recoMu_eta",
      ";SIT matched recoMuon eta;# count",
      100, -3.2, 3.2,
      6, 0, 1, false);

   BookHistArray(h_SIT_recoMu_combIso,
      "h_SIT_recoMu_combIso",
      ";SIT matched recoMuon combIso;# count",
      100, 0., 5.,
      6, 0, 1, false);

   BookHistArray(h_SIT_recoMu_dR,
      "h_SIT_recoMu_dR",
      ";SIT matched recoMuon dR;# count",
      100, 0., 5.,
      6, 0, 1, false);   

   BookHistArray(h_SIT_recoEle_pt,
      "h_SIT_recoEle_pt",
      ";SIT matched recoEle pT;# count",
      100, 0., 100.,
      6, 0, 1, false);

   BookHistArray(h_SIT_recoEle_eta,
      "h_SIT_recoEle_eta",
      ";SIT matched recoEle eta;# count",
      100, -3.2, 3.2,
      6, 0, 1, false);

   BookHistArray(h_SIT_recoEle_combIso,
      "h_SIT_recoEle_combIso",
      ";SIT matched recoEle combIso;# count",
      100, 0., 5.,
      6, 0, 1, false);

   BookHistArray(h_SIT_recoEle_dR,
      "h_SIT_recoEle_dR",
      ";SIT matched recoEle dR;# count",
      100, 0., 5.,
      6, 0, 1, false);   

   BookHistArray(h_genElePt,
      "genElePt",
      ";genElectron Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_genMuPt,
      "genMuPt",
      ";genMuon Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_genTauPt,
      "genTauPt",
      ";genTau Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_delR_eleIT,
      "delR_eleIT",
      ";deltaR(genEle, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_delR_muIT,
      "delR_muIT",
      ";deltaR(genMu, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_delR_tauIT,
      "delR_tauIT",
      ";deltaR(genTau, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);   

   BookHistArray(h_delR_TauEleIT,
      "delR_TauEleIT",
      ";deltaR(genTauEle, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_delR_TauMuIT,
      "delR_TauMuIT",
      ";deltaR(genTauMu, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_delR_TauHadIT,
      "delR_TauHadIT",
      ";deltaR(genTauHad, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_delR_VEleIT,
      "delR_VEleIT",
      ";deltaR(genVEle, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_delR_VMuIT,
      "delR_VMuIT",
      ";deltaR(genVMu, isoTrack);# count",
      100, 0., 10.,
      6, 0, 1, false);

   BookHistArray(h_genPtTauEle,
      "genPtTauEle",
      ";genPtTauEle;# count",
      100, 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_genPtTauMu,
      "genPtTauMu",
      ";genPtTauMu;# count",
      100, 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_genPtTauHad,
      "genPtTauHad",
      ";genPtTauHad;# count",
      100, 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_genPtVEle,
      "genPtVEle",
      ";genPtVEle;# count",
      100, 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_genPtVMu,
      "genPtVMu",
      ";genPtVMu;# count",
      100, 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_genEtaTauEle,
      "genEtaTauEle",
      ";genEtaTauEle;# count",
      100, -3.2, 3.2,
      6, 0, 1, false);

   BookHistArray(h_genEtaTauMu,
      "genEtaTauMu",
      ";genPtTauMu;# count",
      100, -3.2, 3.2,
      6, 0, 1, false);

   BookHistArray(h_genEtaTauHad,
      "genEtaTauHad",
      ";genEtaTauHad;# count",
      100, -3.2, 3.2,
      6, 0, 1, false);

   BookHistArray(h_genEtaVEle,
      "genEtaVEle",
      ";genEtaVEle;# count",
      100, -3.2, 3.2,
      6, 0, 1, false);

   BookHistArray(h_genEtaVMu,
      "genEtaVMu",
      ";genEtaVMu;# count",
      100, -3.2, 3.2,
      6, 0, 1, false);

}


// -----------------------------------------------------------------------------
//
std::ostream& isoTrackPlots::Description( std::ostream& ostrm ) {
   ostrm << "Charm Study Analysis Plots ";
   ostrm << "(bins " << nMin_ << " to " << nMax_ << ") ";
   return ostrm;
}


// -----------------------------------------------------------------------------
// Main module
bool isoTrackPlots::StandardPlots( Event::Data& ev ) {

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

   
   // count number of btagged jets
   int nbjet = 0;
   for(auto jet: ev.JD_CommonJets().accepted){
      if( ev.GetBTagResponse(jet->GetIndex(), bTagAlgo_) > bTagAlgoCut_ ) nbjet++;
   }


   // get generic event variables
   int plotIndex              = (nbjet>4) ? 5 : nbjet;
   double evHT                = ev.CommonHT();
   // double hadronicAlphaT      = ev.HadronicAlphaT();
   // double mht                 = ev.CommonMHT().Pt();
   int nCommJet               = ev.JD_CommonJets().accepted.size();
   vector<double> v_MHTMET    = getMHTandMET( ev );
   int nVertex                = verticesN( ev );
   std::vector< fourMomenta > SIT;


   h_nJets[0]              ->Fill( nCommJet, evWeight );
   h_nBTagJets[0]          ->Fill( nbjet, evWeight );
   h_nVertex[plotIndex]    ->Fill( nVertex, evWeight );
   h_nIsoTrack[plotIndex]  ->Fill( getNIsoTrack( ev ), evWeight );
   h_commHT[plotIndex]     ->Fill( evHT, evWeight );


// fill some isoTrack variables
   unsigned int j=0;
   for(unsigned int i=0; i<ev.pfCandsPt()->size(); i++){
      
      // simulate 5GeV pt cut form SusyCAF
      if (ev.pfCandsPt()->at(i) < 5.) continue;
      
      // stop out of range access
      if (j>=ev.pfCandsP4()->size()) break;

      // fill for all pfCands, pT > 5GeV
      h_pfCandsPt[0]    ->Fill(ev.pfCandsPt()->at(i), evWeight);
      h_pfCandsEta[0]   ->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);
      h_pfCandsDzPV[0]  ->Fill(ev.pfCandsDzPV()->at(i), evWeight);
      h_pfCandsDunno[0] ->Fill((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)), evWeight);
      h_pfCandsCharge[0]->Fill(ev.pfCandsCharge()->at(i), evWeight);

      if (
         (ev.pfCandsPt()->at(i) > 10.) &&
         // (ev.pfCandsP4()->at(j).Eta() < 2.2) &&
         (ev.pfCandsCharge()->at(i) != 0) &&
         (ev.pfCandsDzPV()->at(i) < 0.05)
         ){
         if ((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)) < 0.1){
            // fill if meets isoTrack veto requirements
            h_pfCandsPt[1]    ->Fill(ev.pfCandsPt()->at(i), evWeight);
            h_pfCandsEta[1]   ->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);
            h_pfCandsDzPV[1]  ->Fill(ev.pfCandsDzPV()->at(i), evWeight);
            h_pfCandsDunno[1] ->Fill((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)), evWeight);

            SIT.push_back(ev.pfCandsP4()->at(j));

            // find any gen electrons/muons and plot dR against found isoTrack
            if(!isData_){
               for(auto igen: ev.GenParticles()){
                  if( igen.GetStatus() == 3 ){
                     double isoTDelR = ROOT::Math::VectorUtil::DeltaR(igen, ev.pfCandsP4()->at(j));
                     
                     if( isTrueEle(igen) ){
                        h_delR_eleIT[plotIndex]    ->Fill(isoTDelR, evWeight);
                     }
                     if( isTrueMu(igen) ){
                        h_delR_muIT[plotIndex]     ->Fill(isoTDelR, evWeight);
                     }
                     if( isTrueTau(igen) ){
                        h_delR_tauIT[plotIndex]    ->Fill(isoTDelR, evWeight);
                     }
                     if( isTrueTauEle(ev, igen) ){
                        h_delR_TauEleIT[plotIndex]           ->Fill(isoTDelR, evWeight);
                        if (isoTDelR<0.5) h_nEventsTauEleITMatched[plotIndex]  ->Fill(0.5, evWeight);
                     }
                     if( isTrueTauMu(ev, igen) ){
                        h_delR_TauMuIT[plotIndex]           ->Fill(isoTDelR, evWeight);
                        if (isoTDelR<0.5) h_nEventsTauMuITMatched[plotIndex]  ->Fill(0.5, evWeight);
                     }
                     if( isTrueTauHad(ev, igen) ){
                        h_delR_TauHadIT[plotIndex]           ->Fill(isoTDelR, evWeight);
                        if (isoTDelR<0.5) h_nEventsTauHadITMatched[plotIndex]  ->Fill(0.5, evWeight);
                     }
                     if( isTrueVEle(igen) ){
                        h_delR_VEleIT[plotIndex]          ->Fill(isoTDelR, evWeight);
                        if (isoTDelR<0.5) h_nEventsVEleITMatched[plotIndex] ->Fill(0.5, evWeight);
                     }
                     if( isTrueVMu(igen) ){
                        h_delR_VMuIT[plotIndex]          ->Fill(isoTDelR, evWeight);
                        if (isoTDelR<0.5) h_nEventsVMuITMatched[plotIndex] ->Fill(0.5, evWeight);
                     }

                  }
               } // for igen
            }// !isData_

            // do some gen lepton matching to IT's         
            // fourMomenta genEle = getGenITMatch(ev, 11, ev.pfCandsP4()->at(j));
            // fourMomenta genMu = getGenITMatch(ev, 13, ev.pfCandsP4()->at(j));

            // if (genEle.M() != 0){
            //    // float a, b, d, c;
            //    // genEle.GetCoordinates(a,b,c,d);
            //    // std::cout << "Ele: " << a << " " << b << " " << c << " " << d << std::endl;
               
            //    if( isTrueVEle(genEle) ){
                  
            //    }

            // }
            // if (genMu.M() != 0){

            // }

         }

      }
   } // for pfCands

   if (!isData_){

      // bool counted;
      // for( auto igen: ev.GenParticles() ) {
      //    counted = false;

      //    if( isTrueVEle( igen ) ) h_genElePt[plotIndex]->Fill(igen.Pt(), evWeight);
      //    if( isTrueVMu( igen ) ) h_genMuPt[plotIndex]->Fill(igen.Pt(), evWeight);
      //    if( isTrueTau( igen) ) h_genTauPt[plotIndex]->Fill(igen.Pt(), evWeight);

      //    if( isTrueTauEle(ev, igen) ){
      //       h_nEventsTauEle[plotIndex] ->Fill(0.5, evWeight);
      //       h_genPtTauEle[plotIndex]->Fill(igen.Pt(), evWeight);
      //       h_genEtaTauEle[plotIndex]->Fill(igen.Eta(), evWeight);
      //       counted = true;
      //    }
      //    if( isTrueTauMu(ev, igen) ){
      //       h_nEventsTauMu[plotIndex]  ->Fill(0.5, evWeight);
      //       h_genPtTauMu[plotIndex]->Fill(igen.Pt(), evWeight);
      //       h_genEtaTauMu[plotIndex]->Fill(igen.Eta(), evWeight);
      //       counted = true;
      //    }
      //    if( isTrueTauHad(ev, igen) ){
      //       h_nEventsTauHad[plotIndex] ->Fill(0.5, evWeight);
      //       h_genPtTauHad[plotIndex]->Fill(igen.Pt(), evWeight);
      //       h_genEtaTauHad[plotIndex]->Fill(igen.Eta(), evWeight);
      //       counted = true;
      //    }
      //    if( isTrueVEle(igen) ){
      //       h_nEventsVEle[plotIndex]   ->Fill(0.5, evWeight);
      //       h_genPtVEle[plotIndex]->Fill(igen.Pt(), evWeight);
      //       h_genEtaVEle[plotIndex]->Fill(igen.Eta(), evWeight);
      //       counted = true;
      //    }
      //    if( isTrueVMu(igen) ){
      //       h_nEventsVMu[plotIndex]    ->Fill(0.5, evWeight);
      //       h_genPtVMu[plotIndex]->Fill(igen.Pt(), evWeight);
      //       h_genEtaVMu[plotIndex]->Fill(igen.Eta(), evWeight);
      //       counted = true;
      //    }

      //    if (!counted) h_nEventsOther[plotIndex]->Fill(0.5, evWeight);

      // } // for genParticles

   }

   return true;

}

// -----------------------------------------------------------------------------
// get generator lepton matched to IT
fourMomenta isoTrackPlots::getGenITMatch( Event::Data& ev, int pID, fourMomenta p4IT ){
   
   double dR = .2;
   fourMomenta p4Gen;
   
   // for(auto igen: ev.GenParticles()){

   for(unsigned int i=0; i<ev.GenParticles().size(); i++){

      // if(ev.GenParticles().at(i).Pt()>1.) continue;
      if(ev.GenParticles().at(i).GetStatus() != 3 ) continue;
      if(fabs( ev.GenParticles().at(i).GetID() ) != pID ) continue;
  
      double tmpdR = ROOT::Math::VectorUtil::DeltaR(ev.GenParticles().at(i), p4IT);

      if ( (tmpdR<dR) && (tmpdR>0.) ){
         dR = tmpdR;
         // myMatch = *ev.GenParticles().at(i);
         // std::cout << typeid(ev.GenParticles().at(i)).name() << std::endl;
         // p4Gen = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >::GetCoordinates(ev.GenParticles().at(i));
         // std::cout << typeid(p4Gen).name() << std::endl;
         
         float a,b,c,d;

         ev.GenParticles().at(i).GetCoordinates(a,b,c,d);
         p4Gen.SetCoordinates(a,b,c,d);
      }
   } //loop igen

   if (dR<0.2){
      // std::cout << "DeltaR:   " << dR << std::endl;
      // std::cout << "Ptdiff:   " << p4IT.Pt()-p4Gen.Pt() << std::endl;
      // std::cout << "Etatdiff: " << p4IT.Eta()-p4Gen.Eta() << std::endl;
      // std::cout << "Phidiff:  " << p4IT.Phi()-p4Gen.Phi() << std::endl;
      // std::cout << std::endl;
   }

   return p4Gen;
}

// -----------------------------------------------------------------------------
// Module to get MHT and MET
vector<double> isoTrackPlots::getMHTandMET( Event::Data& ev ){

  vector<double> rev;
  PolarLorentzV mHT(0.,0.,0.,0.);
  LorentzV calomet = LorentzV(*ev.metP4pfTypeI());

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
// Module to get the deltaPhi between two genLevel objects
double isoTrackPlots::getGenDeltaPhi( const Event::GenObject& gOb1, const Event::GenObject& gOb2 ){

   double dPhi = ROOT::Math::VectorUtil::DeltaPhi( gOb1, gOb2 );
   return fabs( dPhi );

}


// -----------------------------------------------------------------------------
// Module to get number of vertices passing quality cuts - from Z. Meng
int isoTrackPlots::verticesN( Event::Data& ev ){
  
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
int isoTrackPlots::getNIsoTrack( Event::Data& ev ){
       
   // if one branch isn't enabled, return true - no pfCands in event
   if (!ev.pfCandsPt.enabled()) return 0;

   /*
    Note: double loop is used due to bad placement of 5GeV pT cut in SusyCAF code.
    P4 and Pt vectors are different lengths.
   */

   int nIso = 0;
   // loop over all pfCands
   
   unsigned int j=0;
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

// -----------------------------------------------------------------------------
// All genMatching code "borrowed" from Z. Meng.
// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueVEle( const Event::GenObject& gob ){
  bool islep=false;
  if(gob.GetStatus() == 3 ) {
    if(fabs( gob.GetID() ) == 11) {
      if(fabs( gob.GetMotherID() ) == 24 || fabs( gob.GetMotherID() ) == 23) {
  islep=true;
      }
    }
  }
  return islep;
}


// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueVMu( const Event::GenObject& gob ){
  bool islep=false;
  if(gob.GetStatus() == 3 ) {
    if(fabs( gob.GetID() ) == 13 ) {
      if(fabs( gob.GetMotherID() ) == 24 || fabs( gob.GetMotherID() ) == 23) {
  islep=true;
      }
    }
  }
  return islep;
}


// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueEle( const Event::GenObject& gob ){
   bool islep=false;
   if(gob.GetStatus() == 3 ) {
      if(fabs( gob.GetID() ) == 11 ) {
          islep=true;
      }
   }
  
  return islep;
}


// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueMu( const Event::GenObject& gob ){
   bool islep=false;
   if(gob.GetStatus() == 3 ) {
      if(fabs( gob.GetID() ) == 13 ) {
          islep=true;
      }
   }
  
  return islep;
}

// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueTau( const Event::GenObject& gob ){
   bool islep=false;
   if(gob.GetStatus() == 3 ) {
      if(fabs( gob.GetID() ) == 15 ) {
          islep=true;
      }
   }
  
  return islep;
}

// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueZMuMu( const Event::GenObject& gob ){
  bool islep=false;
  if(gob.GetStatus() == 3 ) {
    if(fabs( gob.GetID() ) == 13 ) {
      if(fabs( gob.GetMotherID() ) == 23) {
  islep=true;
      }
    }
  }
  return islep;
}

// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueTauEle( Event::Data& ev, const Event::GenObject& gob ){
  bool islep=false;

    //is on-shell
  if( gob.GetStatus() == 3 ) {

    //is a tau
     if( fabs( gob.GetID() ) == 15 ){

      //has lepton daughter
      int truetaulep=0;
      //      vector<int> dID=theDaughterID( &(ev), gob.GetIndex() );
      vector<int> dID=theDaughterID( &(ev), gob.GetID() );
      for( unsigned int i=0; i < dID.size(); i++ ){
  bool islepin=( fabs( dID[i] ) == 11 ) || ( fabs( dID[i] ) == 12 );

  if( islepin ){

    truetaulep++;
  }
      }

      if( truetaulep > 0 ) islep=true;
    }
  }

  return islep;
}


// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueTauMu( Event::Data& ev, const Event::GenObject& gob ){
  bool islep=false;

    //is on-shell
  if( gob.GetStatus() == 3 ) {

    //is a tau
     if( fabs( gob.GetID() ) == 15 ){

      //has lepton daughter
      int truetaulep=0;
      //      vector<int> dID=theDaughterID( &(ev), gob.GetIndex() );
      vector<int> dID=theDaughterID( &(ev), gob.GetID() );
      for( unsigned int i=0; i < dID.size(); i++ ){
  bool islepin=( fabs( dID[i] ) == 13 ) || ( fabs( dID[i] ) == 14 );

  if( islepin ){

    truetaulep++;
  }
      }

      if( truetaulep > 0 ) islep=true;
    }
  }

  return islep;
}

// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueTauHad( Event::Data& ev, const Event::GenObject& gob ){
  bool ishad=false;

    //is on-shell
  if( gob.GetStatus() == 3 ) {

    if( fabs( gob.GetID() ) == 15 ){

      if( gob.Pt() > 0 && fabs( gob.Eta() ) < 15. ){

      //is not true tau lepton
        if( !isTrueTauLep( ev, gob ) ){

    ishad = true;

  }
      }
    }
  }

  return ishad;
}

// -----------------------------------------------------------------------------
//
bool isoTrackPlots::isTrueTauLep( Event::Data& ev, const Event::GenObject& gob ){
  bool islep=false;

    //is on-shell
  if( gob.GetStatus() == 3 ) {

    //is a tau
     if( fabs( gob.GetID() ) == 15 ){

      //has lepton daughter
      int truetaulep=0;
      //      vector<int> dID=theDaughterID( &(ev), gob.GetIndex() );
      vector<int> dID=theDaughterID( &(ev), gob.GetID() );
      for( unsigned int i=0; i < dID.size(); i++ ){
  bool islepin=( fabs( dID[i] ) == 11 ) || ( fabs( dID[i] ) == 12 ) || ( fabs( dID[i] ) == 13 ) || ( fabs( dID[i] ) == 14 );

  if( islepin ){

    truetaulep++;
  }
      }

      if( truetaulep > 0 ) islep=true;
    }
  }

  return islep;
}

// -----------------------------------------------------------------------------
//
std::vector<int> isoTrackPlots::theDaughterID(Event::Data * ev, int mID)//mID is motherID. if use index, it always GetMother()+2=input mother index
{
  std::vector<int> dtype;
  for ( std::vector<Event::GenObject>::const_iterator j = ev->GenParticles().begin();  j != ev->GenParticles().end(); ++j ) {

    //status can not be 3
    if( j->GetStatus()==3 ) continue;

    //has mother
    if( j->GetMother()!=-1 ){

      //mother ID
      //      if(j->GetMother()==index ) {dtype.push_back(j->GetID()); cout<<"ID="<<j->GetID()<<endl;}
      if( j->GetMotherID() == mID ) dtype.push_back( j->GetID() );
    }
  }
  return dtype;
}
