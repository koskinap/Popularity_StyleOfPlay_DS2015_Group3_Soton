%function [y]=style(i)
clear
newData1 = importdata('cleaned_premier_data/classified_dats.csv'); 

A=newData1.data
[m,n]=size(newData1.textdata)
Name=newData1.textdata(1,4:n)

Total_mean= round(mean(A),2)   %For all teams mean  For first conculmn it is the team number ignore it
Total_stand = round(std(A),2)  %For all teams stand deviation   For first conculmn it is the team number ignore it


mean=[]
stand=[]
for i=1:1:20
    [R,~,~]=find(A(:,1)==i)
    matrix=A(R(1,:):R(size(R),:),1:12)
    %mean=[mean;mean(matrix)]
end

%[R,~,~]=find(A(:,1)==1)   %i is the team number change the i value it can change the team number
%matrix=A(R(1,:):R(size(R),:),1:12)


%mean= mean(matrix)         %This is the single team mean
%stand= std(matrix)         %This is the single team stand deviation
%add=[mean;stand]

