%function [y]=style(i)
clear
new_features = importdata('/Users/koskinap/Projects/Popularity_StyleOfPlay_DS2015_Group3_Soton/cleaned_premier_data/classified_data.csv'); 
new_measures = importdata('/Users/koskinap/Projects/Popul       arity_StyleOfPlay_DS2015_Group3_Soton/cleaned_premier_data/merged_data.csv'); 

Measures=new_measures.data
[m_measures,n_measures]=size(new_measures.textdata)
Measures_Name=new_measures.textdata(1,4:n_measures)
[m_measures,n_measures]=size(Measures)
Measures_Total_Data=Measures(:,2:n_measures)


Features=new_features.data
[m_features,n_features]=size(new_features.textdata)
Features_Name=new_features.textdata(1,4:n_features)
[m_features,n_features]=size(Features)
Features_Total_Data=Measures(:,2:n_features)


Measures_mean= mean(Measures)   %For all teams mean  
Measures_stand = std(Measures)  %For all teams stand deviation  

i=2                             %Change the i value to corresponding measures name
j=2                             %Change the i value to corresponding features name


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

h1=histfit(Measures_Total_Data(:,i),2800);
set(h1(1),'Visible','off');
set(h1(2),'Color','g');
hold on ;



x_feasures=Measures_Total_Data(:,j)
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