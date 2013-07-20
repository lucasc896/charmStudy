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
#include <algorithm>

using namespace Operation;

//struct to order on the second entry (dR) in a vector of pairs
struct order_dr_pairs : public std::binary_function<pair<Event::Lepton const*, float>, pair<Event::Lepton const*, float>, bool> {
  bool operator()(const pair<Event::Lepton const*, float>& x, const pair<Event::Lepton const*, float>& y) {
    return ( x.second > y.second ) ;
  }
};

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

   BookHistArray(h_GenEleN,
      "GenEleN",
      ";GenEle N;# count",
      1, 0., 1.,
      6, 0, 1, false);   

   BookHistArray(h_GenMuN,
      "GenMuN",
      ";GenMu N;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_GenTauHadN,
      "GenTauHadN",
      ";GenTauHad N;# count",
      1, 0., 1.,
      6, 0, 1, false);   

   BookHistArray(h_GenOtherN,
      "GenOtherN",
      ";GenOther N;# count",
      1, 0., 1.,
      6, 0, 1, false); 

   BookHistArray(h_GenEleNoMatchN,
      "GenEleNoMatchN",
      ";GenEle NoMatching N;# count",
      1, 0., 1.,
      6, 0, 1, false);   

   BookHistArray(h_GenMuNoMatchN,
      "GenMuNoMatchN",
      ";GenMu NoMatching N;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_GenTauHadNoMatchN,
      "GenTauHadNoMatchN",
      ";GenTauHad NoMatching N;# count",
      1, 0., 1.,
      6, 0, 1, false);   

   BookHistArray(h_GenOtherNoMatchN,
      "GenOtherNoMatchN",
      ";GenOther NoMatching N;# count",
      1, 0., 1.,
      6, 0, 1, false); 

   BookHistArray(h_ITGenEleN,
      "ITGenEleN",
      ";IT Matched GenEle N;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_ITGenElePt,
      "ITGenElePt",
      ";IT Matched GenEle Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_ITGenEleEta,
      "ITGenEleEta",
      ";IT Matched GenEle Eta;# count",
      100., -3., 3.,
      6, 0, 1, false);

   BookHistArray(h_ITGenMuN,
      "ITGenMuN",
      ";IT Matched GenMu N;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_ITGenMuPt,
      "ITGenMuPt",
      ";IT Matched GenMu Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_ITGenMuEta,
      "ITGenMuEta",
      ";IT Matched GenMu Eta;# count",
      100., -3., 3.,
      6, 0, 1, false);

   BookHistArray(h_ITGenHadTauN,
      "ITGenHadTauN",
      ";IT Matched GenHadTau N;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_ITGenHadTauPt,
      "ITGenHadTauPt",
      ";IT Matched GenHadTau Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_ITGenHadTauEta,
      "ITGenHadTauEta",
      ";IT Matched GenHadTau Eta;# count",
      100., -3., 3.,
      6, 0, 1, false);

   BookHistArray(h_ITGenHadTauPtDiff,
      "ITGenHadTauPtDiff",
      ";IT Matched GenHadTau PtDiff;# count",
      60., -30., 30.,
      6, 0, 1, false);

   BookHistArray(h_ITGenOtherN,
      "ITGenOtherN",
      ";IT Matched GenOther N;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_ITGenOtherPt,
      "ITGenOtherPt",
      ";IT Matched GenOther Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_ITGenOtherEta,
      "ITGenOtherEta",
      ";IT Matched GenOther Eta;# count",
      100., -3., 3.,
      6, 0, 1, false);

   BookHistArray(h_ITNoMatchN,
      "ITNoMatchN",
      ";IT No Match N;# count",
      1, 0., 1.,
      6, 0, 1, false);

   BookHistArray(h_ITNoMatchPt,
      "ITNoMatchPt",
      ";IT NoMatch Pt;# count",
      100., 0., 200.,
      6, 0, 1, false);

   BookHistArray(h_ITNoMatchEta,
      "ITNoMatchEta",
      ";IT NoMatch Eta;# count",
      100., -3., 3.,
      6, 0, 1, false);

   // BookHistArray(h_tmpDR,
   //    "tmpDR",
   //    ";dR(SIT, anyLepton);# count",
   //    500., 0., 5,
   //    1, 0, 1, false);

   BookHistArray(h_matchPtDiff,
      "matchPtDiff",
      ";SIT Pt - GenMatch Pt;# count",
      600, -30., 30.,
      1, 0, 1, false);

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

   // count generic event contents (used to calc effs)
   for(auto igen: ev.GenParticles()){
      if( igen.GetStatus() != 3 ) continue;

      if(isTrueTauHad(ev, igen)){
         // In here if gen match is tauhad
         h_GenTauHadN[plotIndex]->Fill(0.5, evWeight);
      }else if(isTrueTauEle(ev, igen) ||
               isTrueVEle(igen)){
         //In here if gen match if tauele or Vele
         h_GenEleN[plotIndex]->Fill(0.5, evWeight);
      }else if(isTrueTauMu(ev, igen) ||
               isTrueVMu(igen)){
         h_GenMuN[plotIndex]->Fill(0.5, evWeight);
      }else{
         h_GenOtherN[plotIndex]->Fill(0.5, evWeight);
      }
   } //igen

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
         (ev.pfCandsDzPV()->at(i) < 0.05) &&
         (ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)) < 0.1){

         /* ##################################### */
         /* ### IF HERE, AN ISOTRACK BE FOUND ### */
         /* ##################################### */


         // fill if meets isoTrack veto requirements
         h_pfCandsPt[1]    ->Fill(ev.pfCandsPt()->at(i), evWeight);
         h_pfCandsEta[1]   ->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);
         h_pfCandsDzPV[1]  ->Fill(ev.pfCandsDzPV()->at(i), evWeight);
         h_pfCandsDunno[1] ->Fill((ev.pfCandsTrkIso()->at(i)/ev.pfCandsPt()->at(i)), evWeight);

         SIT.push_back(ev.pfCandsP4()->at(j));

         // find any gen electrons/muons and plot dR against found isoTrack
         if(!isData_){
            // bool matchedEle = false;
            // fourMomenta genITEleP4 = getGenITMatch(ev, 11, ev.pfCandsP4()->at(j));
            // if (genITEleP4.M()!=0){
            //    // now have a valid SIT matchedEle to generator electron
            //    if (!matchedEle) h_ITGenEleN[plotIndex]->Fill( 0.5, evWeight );
            //    h_ITGenElePt[plotIndex] ->Fill( genITEleP4.Pt(), evWeight );
            //    h_ITGenEleEta[plotIndex]->Fill( genITEleP4.Eta(), evWeight );
            //    // h_ITGenEleIso[plotIndex]->Fill( genITEleP4., evWeight );
            //    matchedEle = true;
            // }

            // bool matchedMu = false;
            // fourMomenta genITMuP4 = getGenITMatch(ev, 13, ev.pfCandsP4()->at(j));
            // if (genITMuP4.M()!=0){
            //    // now have a valid SIT matched to generator electron
            //    if (!matchedMu) h_ITGenMuN[plotIndex]->Fill( 0.5, evWeight );
            //    h_ITGenMuPt[plotIndex]  ->Fill( genITMuP4.Pt(), evWeight );
            //    h_ITGenMuEta[plotIndex] ->Fill( genITMuP4.Eta(), evWeight );
            //    matchedMu = true;
            // }
            

            // bool matchedTau = false;
            // fourMomenta genITTauP4 = getGenITMatch(ev, 15, ev.pfCandsP4()->at(j));
            // if (!matchedEle && !matchedMu){ //check that the event doesn't also contain mu or ele
            //    if (genITTauP4.M()!=0){
            //       if (!matchedTau) h_ITGenHadTauN[plotIndex]->Fill( 0.5, evWeight );
            //       h_ITGenHadTauPt[plotIndex]  ->Fill( genITTauP4.Pt(), evWeight );
            //       h_ITGenHadTauEta[plotIndex] ->Fill( genITTauP4.Eta(), evWeight );
            //       matchedTau = true;
            //    }
            // }

            // if (!matchedEle && !matchedMu && !matchedTau){
            //    h_ITNoMatchN[plotIndex]->Fill( 0.5, evWeight);
            // }


            // std::vector< std::pair<Event::Lepton const*, double> > leptonITdRPairs; 

            // for(auto iele: ev.LD_CommonElectrons().accepted){
            //    double dR = ROOT::Math::VectorUtil::DeltaR(*iele, ev.pfCandsP4()->at(j));
            //    if (dR>=0.5) continue; // veto pair if seperation is too large
            //    // fill vector with the pair of iele and dR
               
            //    std::pair<Event::Lepton const*, double> tmpPair(iele, dR);
            //    leptonITdRPairs.push_back(tmpPair);
            // }
            // for(auto imu: ev.LD_CommonMuons().accepted){
            //    double dR = ROOT::Math::VectorUtil::DeltaR(*imu, ev.pfCandsP4()->at(j));
            //    if (dR>=0.5) continue; // veto pair if seperation is too large
            //    // fill vector with the pair of imu and dR
               
            //    std::pair<Event::Lepton const*, double> tmpPair(imu, dR);
            //    leptonITdRPairs.push_back(tmpPair);
            // }

            // // sort by dR
            // sort(leptonITdRPairs.begin(), leptonITdRPairs.end(), order_dr_pairs());

            // for(UInt_t i=0; i<3; i++){
            //    if (i<leptonITdRPairs.size()){
            //       // std::cout << leptonITdRPairs.at(i).second << std::endl;
            //    }
            // }
            // std::cout << std::endl;

            // std::cout << "Found SIT" << std::endl;

            const Event::GenObject* someMatch = getGenITMatch(ev, ev.pfCandsP4()->at(j));
            if (someMatch){ // in case someMatch is NULL
               // std::cout << ">>> Match details: " << someMatch->Pt() << " " << someMatch->GetID() << std::endl;
               h_matchPtDiff[0]->Fill(ev.pfCandsPt()->at(i) - someMatch->Pt(), evWeight);

               // check if matched gen particle is from tau had
               if(isTrueTauHad(ev, *someMatch)){
                  // In here if gen match is tauhad

                  h_ITGenHadTauN[plotIndex]->Fill(0.5, evWeight);
                  h_ITGenHadTauPt[plotIndex]->Fill(ev.pfCandsPt()->at(i), evWeight);
                  h_ITGenHadTauEta[plotIndex]->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);
                  h_ITGenHadTauPtDiff[plotIndex]->Fill(ev.pfCandsPt()->at(i) - someMatch->Pt(), evWeight);

               }else if(isTrueTauEle(ev, *someMatch) ||
                        isTrueVEle(*someMatch)){
                  //In here if gen match if tauele or Vele

                  h_ITGenEleN[plotIndex]->Fill(0.5, evWeight);
                  h_ITGenElePt[plotIndex]->Fill(ev.pfCandsPt()->at(i), evWeight);
                  h_ITGenEleEta[plotIndex]->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);

               }else if(isTrueTauMu(ev, *someMatch) ||
                        isTrueVMu(*someMatch)){
                  //In here if gen match is taumu or Vmu

                  h_ITGenMuN[plotIndex]->Fill(0.5, evWeight);
                  h_ITGenMuPt[plotIndex]->Fill(ev.pfCandsPt()->at(i), evWeight);
                  h_ITGenMuEta[plotIndex]->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);

               }else{
                  //GenMatch but no process definition

                  h_ITGenOtherN[plotIndex]->Fill(0.5, evWeight);
                  h_ITGenOtherPt[plotIndex]->Fill(ev.pfCandsPt()->at(i), evWeight);
                  h_ITGenOtherEta[plotIndex]->Fill(ev.pfCandsP4()->at(j).Eta(), evWeight);

               }

            }else{
               //No gen match to SIT
               h_ITNoMatchN[0]->Fill(0.5, evWeight);
            }

            // for(auto igen: ev.GenParticles()){
            //    if( igen.GetStatus() != 3 ) continue;
            //    int thisID = fabs( igen.GetID() );

            //    // check for Lepton match
            //    if(   (thisID == 11) ||
            //          (thisID == 13) ||
            //          (thisID == 15) ){

            //       double tmpdR = ROOT::Math::VectorUtil::DeltaR(igen, ev.pfCandsP4()->at(j));
            //       h_tmpDR[0]->Fill(tmpdR, evWeight);
            //    }
            // }
       
            for(auto igen: ev.GenParticles()){
               if( igen.GetStatus() != 3 ) continue;

               if(isTrueTauHad(ev, igen)){
                  // In here if gen match is tauhad
                  h_GenTauHadNoMatchN[plotIndex]->Fill(0.5, evWeight);
               }else if(isTrueTauEle(ev, igen) ||
                        isTrueVEle(igen)){
                  //In here if gen match if tauele or Vele
                  h_GenEleNoMatchN[plotIndex]->Fill(0.5, evWeight);
               }else if(isTrueTauMu(ev, igen) ||
                        isTrueVMu(igen)){
                  h_GenMuNoMatchN[plotIndex]->Fill(0.5, evWeight);
               }else{
                  h_GenOtherNoMatchN[plotIndex]->Fill(0.5, evWeight);
               }
            }
         }// !isData_
      } // end of found isoTrack loop
   } // for pfCands

   return true;

}

// -----------------------------------------------------------------------------
// get generator lepton matched to IT
const Event::GenObject* isoTrackPlots::getGenITMatch( Event::Data& ev, fourMomenta p4IT ){
   // std::cout << "Checking for match." << std::endl;
   double dR = .2;
   const Event::GenObject *gMatch=NULL;

   for(unsigned int i=0; i<ev.GenParticles().size(); i++){

      // if(ev.GenParticles().at(i).Pt()>1.) continue;
      if( ev.GenParticles().at(i).GetStatus() != 3 ) continue;

      // check for Lepton match
      int thisID = fabs( ev.GenParticles().at(i).GetID() );
      if(   (thisID == 11) ||
            (thisID == 13) ||
            (thisID == 15) ){
  
         double tmpdR = ROOT::Math::VectorUtil::DeltaR(ev.GenParticles().at(i), p4IT);
         if ( (tmpdR<dR) && (tmpdR>0.) ){
            // found a closer match
            dR = tmpdR;
            gMatch = &ev.GenParticles().at(i);
         }
      }
   } //loop igen

   if (dR<0.2){

      // std::cout << "Found match!" << std::endl;
      // std::cout << "DeltaR:   " << dR << std::endl;
      // std::cout << "Ptdiff:   " << p4IT.Pt()-p4Gen.Pt() << std::endl;
      // std::cout << "Etatdiff: " << p4IT.Eta()-p4Gen.Eta() << std::endl;
      // std::cout << "Phidiff:  " << p4IT.Phi()-p4Gen.Phi() << std::endl;
      // std::cout << std::endl;
   }

   return gMatch;
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
