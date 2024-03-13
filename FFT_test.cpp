#include <iostream>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "TCanvas.h"
#include "TROOT.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TLegend.h"
#include "TArrow.h"
#include "TMath.h"
#include "TVirtualFFT.h"
#include "TGraph.h"
#include "TVirtualFFT.h"
   
void FFT_test(){   

    TFile* _file0 = TFile::Open("Ana_MSU/Jordan_Run2452.root");
    gROOT->ProcessLine( "gErrorIgnoreLevel = 2001;");
    ofstream cfile ("NoBeam_Data.csv"); 
    TList *Trace = (TList*)gROOT->FindObject("FusionTraces");
   
    int event_num = Trace->GetEntries();

    int loop = 100000;
  
    //std::vector<TCanvas*> can_fftr(event_num);
    
    int counter =0; 
    double x[20] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
    int b_cnt =0;
    int toob=0;
    int ok=0;
    for(int evt=0; evt<event_num;evt++){
        if(evt%10000==0){
            std::cout << "reading event " << evt << std::endl;
        }
        //TCanvas *c2 = new TCanvas(("Real Part of event "+std::to_string(counter)).c_str());
       
        //c2->Divide(2,2);
        //can_fftr[counter]=c2;
       
        
        int lg=0;
        //can_fftr[counter]->cd(1);
        TGraph *fusg = (TGraph*)Trace->At(evt);
        Double_t *in = fusg->GetY();
        TGraph *n_fus = new TGraph(20,x,in);
        n_fus->SetMaximum(6);
        Double_t *in2 = n_fus->GetY();
        for(int i=0; i<20; i++){
           
            if(in[i]>10){
                lg=1;
            }
        }
        if(lg==1){
            toob+=1;
        }
        else{
            ok+=1;
        }
        //n_fus->Draw();
        //printing is not matching what is happening 
        
        //this also skips the not fusion elements, might be find now to get a quick overview but next should come after nf events 
        //fusg->SetTitle("Event");
        //fusg->Draw();
        
        Int_t n_size = 20;
        TVirtualFFT *fft_own = TVirtualFFT::FFT(1, &n_size, "R2C ES K");
        if (!fft_own) continue;
        fft_own->SetPoints(in);
        fft_own->Transform();
        
        //Copy all the output points:
        fft_own->GetPoints(in);
        //Draw the real part of the output
        //can_fftr[counter]->cd(2);
        TH1 *hr = nullptr;
        hr = TH1::TransformHisto(fft_own, hr, "RE");
        hr->SetTitle("Real part of the fusion transform");
        hr->Draw();
        hr->SetStats(kFALSE);
        hr->GetXaxis()->SetLabelSize(0.05);
        hr->GetYaxis()->SetLabelSize(0.05);
        //can_fftr[counter]->cd(3);
        TH1 *him = nullptr;
        him = TH1::TransformHisto(fft_own, him, "IM");
        him->SetTitle("Im. part of the fusion transform");
        him->Draw();
        him->SetStats(kFALSE);
        him->GetXaxis()->SetLabelSize(0.05);
        him->GetYaxis()->SetLabelSize(0.05);
        counter+=1;
        //delete in;
        delete fft_own;


        int bin_max = him->GetMaximumBin();
        int bin_min = him->GetMinimumBin();
        double im_max = (him->GetBinContent(bin_max))*(him->GetBinContent(bin_max));
        double im_min = (him->GetBinContent(bin_min))*(him->GetBinContent(bin_min));
        
        delete him;
        delete hr;
       

        //only printing beam events hopefully 
        if(im_min>5){
            b_cnt+=1;
            if(b_cnt==1){
                //can_fftr[counter-1]->SaveAs(Form("FFT_noBeam.pdf("));
                //ncan_fftim[nf_c-1]->SaveAs(Form("FFT.pdf");
            }
            else{
                //can_fftr[counter-1]->SaveAs(Form("FFT_noBeam.pdf"));
                //ncan_fftim[nf_c-1]->SaveAs(Form("FFT.pdf"));
            }
            for (int i=0; i<20; i++){
                if(i<19){
                    cfile << in2[i] << ", ";
                }
                else{
                    cfile << in2[i] << endl;
                }

                
            }
        }
        
    }
        
        
        
    

    //can_fftr[counter-2]->SaveAs(Form("FFT_noBeam.pdf)"));
    std::cout << b_cnt << std::endl;
    std::cout << "too large " << toob << std::endl;
    std::cout << "ok" << ok << std::endl;
    cfile.close();

}