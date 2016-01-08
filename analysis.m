%function [y]=style(i)
clear
new_features = importdata('/Users/fei_Daniel/Desktop/Style of play/classified_data2.csv'); 
new_measures = importdata('/Users/fei_Daniel/Desktop/Style of play/merged_data.csv'); 


Measures=new_measures.data
[m_measures,n_measures]=size(new_measures.textdata)
Measures_Name=new_measures.textdata(1,4:n_measures)
[m_measures,n_measures]=size(Measures)
Measures_Total_Data=Measures(:,2:n_measures)


Features=new_features.data
[m_features,n_features]=size(new_features.textdata)
Features_Name=new_features.textdata(1,4:n_features)
[m_features,n_features]=size(Features)
Features_Total_Data=Features(:,2:n_features)



Measures_mean= mean(Measures)   %For all teams mean  
Measures_stand = std(Measures)  %For all teams stand deviation

Features_mean= mean(Features)  
Features_stand = std(Features) 

Total_matrix=[Measures_mean;Measures_stand]


i=5                             %Change the i value to corresponding measures name
j=1                             %Change the i value to corresponding features name




[R,~,~]=find(Measures(:,1)==1)   %i is the team number change the i value it can change the team number
matrix=Measures(R(1,:):R(size(R),:),1:12)

mean= mean(matrix)         %This is the single team mean
stand= std(matrix)         %This is the single team stand deviation




%CVX tool to find the weight of linear regression of FEATURES

% Load Boston Housing Data from UCI ML Repository
%
%load -ascii housing.data;
% Normalize the data, zero mean, unit standard deviation
%
[N, p1] = size(Features);
p = p1-1;
Y = [Features(:,2:p) ones(N,1)];
for j=1:1:p-1
Y(:,j)=Y(:,j)-mean(Y(:,j));
Y(:,j)=Y(:,j)/std(Y(:,j));
end
f = Features(:,p1);
f = f - mean(f);
f = f/std(f);

%cvx_begin quiet
%variable w2(p);
%minimize( norm(Y*w2-f));
%cvx_end



%pseudo inverse
w = inv(Y'*Y)*Y'*f;







%CVX tool to find the weight of linear regression of MEASURES

% Load Boston Housing Data from UCI ML Repository
%
%load -ascii housing.data;
% Normalize the data, zero mean, unit standard deviation
%
%[N, p1] = size(Measures);
%p = p1-1;
%Y = [Measures(:,2:p) ones(N,1)];
%for j=1:1:p-1
%Y(:,j)=Y(:,j)-mean(Y(:,j));
%Y(:,j)=Y(:,j)/std(Y(:,j));
%end
%f = Measures(:,p1);
%f = f - mean(f);
%f = f/std(f);

%cvx_begin quiet
%variable w2(p);
%minimize( norm(Y*w2-f));
%cvx_end


%pseudo inverse
%w = inv(Y'*Y)*Y'*f;






%find the weight of linear regression of MEASURES using random matrix


%[N, p1] = size(Measures);
%p = p1-1;


%B=randperm(N);
%Measures = Measures(B,:);


%Y = [Measures(:,2:p) ones(N,1)];

%for j=1:1:p-1
%Y(:,j)=Y(:,j)-mean(Y(:,j));
%Y(:,j)=Y(:,j)/std(Y(:,j));
%end
%f = Measures(:,p1);
%f = f - mean(f);
%f = f/std(f);

%for i=1:1:350
%    Y_training(i,:)=Y(i,:)
%    f_training(i,:)=f(i,:)
%end

%for i=1:1:N-350
%    Y_test(i,:)=Y(i+350,:)
%    f_test(i,:)=f(i+350,:)
%end

%w = inv(Y_training'*Y_training)*Y_training'*f_training;


%Measures_test=Y_test*w

%scatter(Measures_test,f_test)
%hold on

%xx=[-1.5:0.01:1.5]
%yy=xx
%plot(xx,yy)
%xlabel('caculate popularity'),ylabel('original popularity')  





%Calculate the correlaion

corelation_matrix_1=[]
corelation_matrix_2=[]



%Corelation of features
for i=1:1:n_features-1
    corelation_matrix_2(:,i)=corr(Features_Total_Data(:,i),Features_Total_Data(:,n_features-1))
end


Corelation of measures
for i=1:1:n_measures-1
    corelation_matrix_2(:,i)=corr(Measures_Total_Data(:,i),Measures_Total_Data(:,n_measures-1))
end




x_Measures=Measures_Total_Data(:,i)
x_Measures=sort(x_Measures);
d_Measures=diff([x_Measures;max(x_Measures)+1]);
count = diff(find([1;d_Measures])) ;
y_Measures =[x_Measures(find(d_Measures)) count]

figure (1)
[Measures,b]=hist(Measures_Total_Data(:,i));
bar(b,Measures/sum(Measures));
xlabel(Measures_Name(1,i+1)),ylabel('probability')  
hold on

h1=histfit(Measures_Total_Data(:,i),2800);
set(h1(1),'Visible','off');
set(h1(2),'Color','g');
hold on ;


figure (2)
bar(y_Measures(:,1),y_Measures(:,2)/sum(y_Measures(:,2)));
xlabel(Measures_Name(1,i+1)),ylabel('probability')  
hold on;

h1=histfit(Measures_Total_Data(:,i),7000);
set(h1(1),'Visible','off');
set(h1(2),'Color','g');
hold on ;



%Bar mid point plots
CFT_x=y_Measures(:,1)
CFT_Y=y_Measures(:,2)/sum(y_Measures(:,2))
plot(y_Measures(:,1),y_Measures(:,2)/sum(y_Measures(:,2)),'r','LineWidth',3);

x_feasures=Features_Total_Data(:,j)
x_feasures=sort(x_feasures);
d_features=diff([x_feasures;max(x_feasures)+1]);
count = diff(find([1;d_features])) ;
y_feasures =[x_feasures(find(d_features)) count]

figure (3)
[Measures,b]=hist(Measures_Total_Data(:,j));
bar(b,Measures/sum(Measures));
xlabel(Features_Name(1,j+1)),ylabel('probability')  
hold on

h1=histfit(Measures_Total_Data(:,j),2800);
set(h1(1),'Visible','off');
set(h1(2),'Color','g');
hold on ;

figure (4)
bar(y_feasures(:,1),y_feasures(:,2)/sum(y_feasures(:,2)));
xlabel(Features_Name(1,j+1)),ylabel('probability')  
hold on;

h1=histfit(Measures_Total_Data(:,j),2800);
set(h1(1),'Visible','off');
set(h1(2),'Color','g');
hold on ;







%Three dimension points plot
for i=1:1:m_features
    z(i,:)=i
end

scatter3(z,Features(:,2),Features(:,7))