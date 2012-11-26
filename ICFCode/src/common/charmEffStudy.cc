#include "charmEffStudy.hh"
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
charmEffStudy::charmEffStudy( const Utils::ParameterSet& ps ) :
// Misc
   dirName_( ps.Get<std::string>("DirName") ),
   nMin_( ps.Get<int>("MinObjects") ),
   nMax_( ps.Get<int>("MaxObjects") ),
   bTagAlgo_( ps.Get<int>("BTagAlgo") ),
   bTagAlgoCut_( ps.Get<double>("BTagAlgoCut") ),
   minDR_( ps.Get<double>("minDR") ),
   StandardPlots_( ps.Get<bool>("StandardPlots") )

   { 
   }

// -----------------------------------------------------------------------------
//
charmEffStudy::~charmEffStudy() {}

// -----------------------------------------------------------------------------
//
void charmEffStudy::Start( Event::Data& ev ) {
   initDir( ev.OutputFile(), dirName_.c_str() );
   BookHistos();
}

// -----------------------------------------------------------------------------
//
void charmEffStudy::BookHistos() {
   if ( StandardPlots_ ){ StandardPlots(); }

}

// -----------------------------------------------------------------------------
//
bool charmEffStudy::Process( Event::Data& ev ) {
   if ( StandardPlots_ ){ StandardPlots(ev); }
   return true;
}



// -----------------------------------------------------------------------------
//
void charmEffStudy::StandardPlots() {

   BookHistArray(h_nJets,
     "n_Jets",
     ";nJets;# count",
     12, 0., 12.,
     1, 0, 1, true);

   BookHistArray(h_nJetsMatchB,
     "n_JetsMatchB",
     ";nJets;# count",
     12, 0., 12.,
     1, 0, 1, false);
 
   BookHistArray(h_nJetsMatchC,
     "n_JetsMatchC",
     ";nJets;# count",
     12, 0., 12.,
     1, 0, 1, false);

   BookHistArray(h_nJetsMatchL,
     "n_JetsMatchL",
     ";nJets;# count",
     12, 0., 12.,
     1, 0, 1, false);

   BookHistArray(h_jetFlavour,
      "jetFlavour",
      ";pdgId;# count",
      200, 0., 200.,
      4, 0, 1, false);

   BookHistArray(h_charmJetdR1,
      "charmJetdR1",
      ";DeltaR;# count",
      50, 0., 10.,
      4, 0, 1, false);

   BookHistArray(h_charmJetdR2,
      "charmJetdR2",
      ";DeltaR;# count",
      50, 0., 10.,
      4, 0, 1, false);

   BookHistArray(h_nBTagJets,
      "n_BTagged_Jets",
      ";nBJets;# count",
      6, 0., 6.,
      3, 0, 1, false);

   BookHistArray(h_nBTagJetsMatchB,
     "n_BTagged_JetsMatchB",
     ";nBJets;# count",
     6, 0., 6.,
     3, 0, 1, false);
 
   BookHistArray(h_nBTagJetsMatchC,
     "n_BTagged_JetsMatchC",
     ";nBJets;# count",
     6, 0., 6.,
     3, 0, 1, false);

   BookHistArray(h_nBTagJetsMatchL,
     "n_BTagged_JetsMatchL",
     ";nBJets;# count",
     6, 0., 6.,
     3, 0, 1, false);   

   BookHistArray(h_nTrueB,
     "n_Truth_B",
     ";nTrueBJets;# count",
     6, 0., 6.,
     1, 0, 1, true);
 
   BookHistArray(h_nTrueC,
     "n_Truth_C",
     ";nTrueCJets;# count",
     6, 0., 6.,
     1, 0, 1, true);
   
   BookHistArray(h_noMatch_response,
      "jet_response",
      ";BTagger Descriminant;# count",
      1000, 0., 10.,
      5, 0, 1, false);

   BookHistArray(h_bMatched_response,
      "bMatched_response",
      ";BTagger Descriminant;# count",
      1000, 0., 10.,
      5, 0, 1, false);

   BookHistArray(h_cMatched_response,
      "cMatched_response",
      ";BTagger Descriminant;# count",
      1000, 0., 10.,
      5, 0, 1, false);

   BookHistArray(h_lMatched_response,
      "lMatched_response",
      ";BTagger Descriminant;# count",
      1000, 0., 10.,
      5, 0, 1, false);

   BookHistArray(h_charmEtaSign,
      "charmEtaSign",
      ";blah;# count",
      2, 0., 2.,
      1, 0, 1, false);
}


// -----------------------------------------------------------------------------
//
std::ostream& charmEffStudy::Description( std::ostream& ostrm ) {
   ostrm << "Charm tag efficiency study ";
   ostrm << "(bins " << nMin_ << " to " << nMax_ << ") ";
   return ostrm;
}


// -----------------------------------------------------------------------------
//
bool charmEffStudy::StandardPlots( Event::Data& ev ) {
// main module

   unsigned int nobjkt = ev.CommonObjects().size();
   int nbjet[3], nbjetMatchB[3], nbjetMatchC[3], nbjetMatchL[3];
   int njet=0, nJetMatchB=0, nJetMatchC=0, nJetMatchL=0;
   double bTagAlgoCut[3]={.898,.679,.244};

   for(int i=0; i<3; i++){
      nbjetMatchB[i]=0;
      nbjetMatchC[i]=0;
      nbjetMatchL[i]=0;
      nbjet[i]=0;
   }

   // a couple event level vetoes
   if (!StandardPlots_) return true;
   if( nobjkt < nMin_ || nobjkt > nMax_ ) return true;


   // loop over common jets
   for(unsigned int i=0; i<ev.JD_CommonJets().accepted.size(); i++) {
      njet++;
      
      //match generic jets to partons
      if( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 5, minDR_) ) nJetMatchB++;
      if( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 4, minDR_) ) nJetMatchC++;
      if( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 3, minDR_) || matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 2, minDR_) || matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 1, minDR_) ){
         nJetMatchL++;
      }

      // loop over Tgt/Med/Lse
      for(int j=0; j<3; j++){
         if(ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), bTagAlgo_) > bTagAlgoCut[j]){
            nbjet[i]++;
            if( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 5, minDR_) ) nbjetMatchB[j]++;
            if( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 4, minDR_) ) nbjetMatchC[j]++;
            if( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 3, minDR_) || matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 2, minDR_) || matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 1, minDR_) ){
               nbjetMatchL[j]++;
            }
         }
      }

      //look for b and c quark matching
      if ( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 5, minDR_) ){
         h_bMatched_response[0]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) );
         h_bMatched_response[1]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 6) );
         h_bMatched_response[2]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 7) );
         h_bMatched_response[3]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 8) );
         h_bMatched_response[4]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 2) );
      }
      if ( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 4, minDR_) ){
         h_cMatched_response[0]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) );
         h_cMatched_response[1]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 6) );
         h_cMatched_response[2]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 7) );
         h_cMatched_response[3]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 8) );
         h_cMatched_response[4]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 2) );     
      }
      if( matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 3, minDR_) || matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 2, minDR_) || matchedToGenQuark(ev, (*ev.JD_CommonJets().accepted.at(i)), 1, minDR_) ){
         h_lMatched_response[0]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) );
         h_lMatched_response[1]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 6) );
         h_lMatched_response[2]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 7) );
         h_lMatched_response[3]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 8) );
         h_lMatched_response[4]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 2) );
      }

      //fill for any jet
        h_noMatch_response[0]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 5) );
        h_noMatch_response[1]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 6) );
        h_noMatch_response[2]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 7) );
        h_noMatch_response[3]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 8) );
        h_noMatch_response[4]->Fill( ev.GetBTagResponse(ev.JD_CommonJets().accepted.at(i)->GetIndex(), 2) );
   }

   // fill jet multiplicities
   h_nJets[0]->Fill(njet);
   h_nJetsMatchB[0]->Fill(nJetMatchB);
   h_nJetsMatchC[0]->Fill(nJetMatchC);
   h_nJetsMatchL[0]->Fill(nJetMatchL);

   
   for(int i=0; i<3; i++){
      h_nBTagJets[i]->Fill(nbjet[i]);
      h_nBTagJetsMatchB[i]->Fill(nbjetMatchB[i]);
      h_nBTagJetsMatchC[i]->Fill(nbjetMatchC[i]);
      h_nBTagJetsMatchL[i]->Fill(nbjetMatchL[i]);
   }

   // get the two genCharms
   Event::GenObject gCharm1(0.,0.,0.,0.,0,0,0,0);
   Event::GenObject gCharm2(0.,0.,0.,0.,0,0,0,0);
   for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ){
      if( (*igen).GetStatus() == 3 ){   
         if( (fabs((*igen).GetID()) == 4) && ((*igen).GetMotherID() == 1000006) )         gCharm1 = *igen;
         if( (fabs((*igen).GetID()) == 4) && ((*igen).GetMotherID() == -1000006) )        gCharm2 = *igen;
      }

   }

   if ((gCharm1.Eta()>0.) && (gCharm2.Eta()<0.)){
      h_charmEtaSign[0]->Fill(1.5);
   }
   else if ((gCharm2.Eta()>0.) && (gCharm1.Eta()<0.)){
      h_charmEtaSign[0]->Fill(1.5);
   }
   else{
      h_charmEtaSign[0]->Fill(0.5);
   }
   
   for(unsigned int i=0; i<4; i++){
      if (ev.JD_CommonJets().accepted.size()>i){
         h_jetFlavour[i]   ->Fill( getJetFlavour(ev, *ev.JD_CommonJets().accepted.at(i), minDR_) );
         h_charmJetdR1[i]  ->Fill( getDeltaR(gCharm1,*ev.JD_CommonJets().accepted.at(i)) );
         h_charmJetdR2[i]  ->Fill( getDeltaR(gCharm2,*ev.JD_CommonJets().accepted.at(i)) );
      }
   }


   //check for truth b
   if( hasTrueQuark(ev, 5) ){
      int numTrue   = numTrueQuarks(ev, 5);
      h_nTrueB[0] ->Fill( numTrue );
   }

   //check for truth c
   if( hasTrueQuark(ev, 4) ){
      int numTrue   = numTrueQuarks(ev, 4);
      h_nTrueC[0] ->Fill( numTrue );
   }

   return true;

}


// -----------------------------------------------------------------------------
//
bool charmEffStudy::hasTrueQuark( const Event::Data& ev, int pdgID ) {
// check if an event has a genLevel quark of certain pdgID

   for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ) {

      if( fabs((*igen).GetID()) == pdgID ){
         if( (*igen).GetStatus() == 3 ){
            return true;
         }
      }
   }
   
   return false;

}


// -----------------------------------------------------------------------------
//
int charmEffStudy::numTrueQuarks( const Event::Data& ev, int pdgID) {
// count number of genLevel quarks of certain pdgID in event

   int nParticle=0;

   for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ) {
  
      if( fabs((*igen).GetID()) == pdgID ){
         if( (*igen).GetStatus() == 3 ){
            nParticle++;
         }
      }
   }
   
   return nParticle;

}


// -----------------------------------------------------------------------------
//
bool charmEffStudy::matchedToGenQuark( const Event::Data& ev, const Event::Jet &jet, int pdgID, float minDR ){
// check if passed jet is matched to genLevel quark of certain pdgID, in cone minDR

   for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ) {

      if( fabs((*igen).GetID()) == pdgID ){
         if( (*igen).GetStatus() == 3 ){
            if( fabs(ROOT::Math::VectorUtil::DeltaR( (*igen),jet) ) < minDR ) return true;
         }
      }

   }

   return false;
}


// -----------------------------------------------------------------------------
//
int charmEffStudy::getJetFlavour( const Event::Data& ev, const Event::Jet &jet, float minDR ){

   float myPdgId=-1;

   for( std::vector<Event::GenObject>::const_iterator igen = ev.GenParticles().begin(); igen != ev.GenParticles().end(); ++igen ) {
      if( (*igen).GetStatus() == 3 ){
         if( fabs(ROOT::Math::VectorUtil::DeltaR( (*igen),jet) ) < minDR ){
            myPdgId=(*igen).GetID();
         }
      }
   }

   return myPdgId;
}


// -----------------------------------------------------------------------------
//
float charmEffStudy::getDeltaR( const Event::GenObject gOb, const Event::Jet &jet ){

   return ROOT::Math::VectorUtil::DeltaR(gOb, jet);

}

