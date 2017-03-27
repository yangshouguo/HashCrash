#include<iostream>
#include<fstream>
#include<string.h>
#include<string>
#include<stdio.h>
using namespace std;
#define instr_MAX_LEN 128
#define instr_MAX_NUM 500
char simil[instr_MAX_LEN];
int N,L,realL;
void getmax_withmask();
char instr[instr_MAX_NUM][instr_MAX_LEN];
char final_mask[instr_MAX_LEN];//temp vir for keep tmp mask 
bool readfile (const char *);
void findsimbit();
void print_mask(char *);
bool select_mask();
void and_op(char * , char *);
void findmaxset();
int instr_real_num ;
void findsimbit();
void mask_cpy(char* ,const char *);
typedef struct xx{
    char after_and[instr_MAX_LEN];
    int setnum ;
}afterAndsame;
afterAndsame result;
char result_mask[instr_MAX_LEN];//record the output mask
afterAndsame samearr[instr_MAX_NUM];
int main(int argc ,char ** arg ){
    
    if(argc < 3){
        cout<<"no parameter!"<<endl;
        return 0;
    }else{
       // cout<<arg[0]<<arg[1]<<":"<<arg[2]<<endl;
        sscanf(arg[1],"%d",&N);
    }
    result.setnum = 0 ;
    if(!readfile (arg[2])){

        cout<<"open file failed\n";
        return 0;
    }
       findsimbit();
    if(N>L){
        cout<<"input  is not reasonable(too big)\n";
        return 0;
    }
    if( select_mask() ){
               // and_op();
               // findmaxset();
       // cout<<"result_mask  :";
       // print_mask(result_mask);
       // cout<<endl;
       // cout<<"number :"<<result.setnum<<endl;
       // cout<<"result :";
        for(int i = 0 ; i < realL ; ++i){
            if(!simil[i]){
            cout<<instr[0][i];
            continue; 
            }else{
                
                if(result_mask[i]==0){
                    cout<<result.after_and[i];

                }else{
                    cout<<"x";
                }

            }

        }
        cout<<endl;
    }


}
bool readfile(const char *  filename){
    ifstream infile(filename);
    if(!infile.is_open()){
        cout<<"file open failed"<<endl;
        return 0;
    }
    int i = 0 ;
    while (!infile.eof()){
        infile>>instr[i++];
       // cout << instr[i-1]<<endl;
    }
    instr_real_num = i-1 ;
   // cout<<"read "<<instr_real_num<<" instruction"<<endl;
    return 1;
}
bool flag[instr_MAX_LEN];//1 means a mask bit set in there
void dfs(int n,int start){
    //cout<<"in dfs n,start:";
    //cout<<n<<","<<start<<endl;
    //getchar();
    if (n== N){
       // cout<<"final_mask is :";
       // print_mask(final_mask);
       // cout<<endl;
        getmax_withmask();
    }else{
        for (int i = start ; i<realL ; ++i){
            if(realL - start < N - n+1)
                break;
            if (flag[i]==0 && simil[i]==1){
                final_mask[i] = 1;
                flag[i] = 1;
                dfs(n+1,i+1);
                flag[i] = 0;
                final_mask[i] = 0;
            }
        } 
    }
}
bool select_mask(){
    memset(final_mask , 0 , sizeof final_mask);
    //select N index which is not 0 in simil
    memset(flag ,0 , sizeof flag);
    dfs(0,0);
}
void print_mask(char * mask){
    for (int i = 0 ; i < realL ; ++i)
        cout<<(int)mask[i];
}
void getmax_withmask(){
    memset(samearr,0,sizeof samearr);
   int setnum_tmp = 0 ;
    bool isInsert = false;
   char afterAndchar[instr_MAX_LEN];
    afterAndsame tmp ;
    tmp.setnum = 0 ;
    for (int i = 0 ; i < instr_real_num; ++i){
        and_op(instr[i],afterAndchar);
       // cout<<"afterAndchar : "<<afterAndchar<<endl;
        isInsert = false;
        for (int j = 0 ; j < setnum_tmp ; ++j){
           // cout<<"cmp with : " << samearr[j].after_and <<endl;
            if(!strcmp(afterAndchar , samearr[j].after_and)){
               // cout<<afterAndchar <<" == "<<samearr[j].after_and<<endl;
                samearr[j].setnum++;
                if(tmp.setnum < samearr[j].setnum){
                    tmp.setnum = samearr[j].setnum;
                    strcpy(tmp.after_and , samearr[j].after_and);
                }
                isInsert = true;
                break;
            }
        }
        if(!isInsert){
            
            strcpy(samearr[setnum_tmp].after_and , afterAndchar);
            samearr[setnum_tmp].setnum++;
           // cout<<"insert "<<afterAndchar<<" to "<<samearr[setnum_tmp].after_and<<endl;
            setnum_tmp++;
        }
    }
    if(!tmp.setnum){
        tmp.setnum = 1;
        strcpy(tmp.after_and,samearr[0].after_and);
    }
    if(result.setnum<tmp.setnum){
        
        mask_cpy(result_mask , final_mask);
        result.setnum = tmp.setnum;
        strcpy(result.after_and , tmp.after_and);
       // cout<<"change max :";
       // print_mask(result_mask);
       // cout<<" ";
       // print_mask(final_mask);
       // cout<<"after_and : "<<tmp.after_and;
       // cout<<endl;
    }
}
void and_op(char *instr , char * afterAnd){
    for (int i = 0 ; i < realL ; ++i){
        if(!simil[i]){

            afterAnd[i] = '0';
            continue;
        }
        if(instr[i]=='0' || final_mask[i] )
            afterAnd[i] = '0';
        else
            afterAnd[i] = '1';
    }
    afterAnd[realL] = 0;
   // cout<<"and_op : afterAnd :"<<afterAnd<<endl;
}
void mask_cpy(char * a, const char * b){
    for (int i = 0 ; i < realL ; ++i)
        a[i] = b[i];
}
void findsimbit(){
    realL = strlen(instr[0]);
    L = 0 ;
   // cout<<"instruction length is :"<<realL<<endl;
    for (int i = 0 ; i < realL ; ++i ){
        simil[i] = 0;
        for (int j = 0 ; j < instr_real_num-1 ; ++j){
            if (instr[j][i]!=instr[j+1][i]){
                simil[i] = 1;
                L++;
                break;

            }
        }
    }
   // cout<<"isntruction simil_mask is:";
   // for (int i = 0 ; i < realL ; ++i){
    //    cout<<int(simil[i]);
    //}
   // cout<<"\n";
   // cout<<"different bits :"<<L<<endl;
   // cout<<endl;

}
