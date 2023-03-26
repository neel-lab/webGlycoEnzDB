% This is a program used to convert 'finishedGlycogenes.xlsx' (part of
% GlycoEnzOnto) into a hierarchy that is displayed at GlycoEnzDB. There are
% three parts of the program: a) 'getKeyValues' to determine unique
% pathways/functions in GlycoEnzOnto; and b) 'makeH' to add genes to the
% pathway/function hierarchy in order to populate the fields in the actual
% website. iii) arrangeHierarchy to format files that are used by the
% Django app.
% There are two input files: i) 'finishedGlycogenes.xlsx' that contains
% the ontology data; ii) inputData.xlsx that contains a) dictionary 
% nomeclature to convert GlycoEnzOnto into GlycoEnzDB format (minor changes
% in text); and b) Hierarchy data which contains the actual hierarchy that is
% implemented online; and c) a dictionary to convert members names to
% webFormat.

% Authors: Sriram Neelamegham 
% Created: 02/12/2023
% Last modified: 03/26/2023

clear;
Program='reorganize';  % choices here are 'getKeyValue','reorganize' and anything else
if strmatch(Program,'getKeyValue')
    out=getKeyValue('function');  % input is either 'pathway' or 'function' depending on what column of 'finishedGlycogenes.xlsx' is to be read
elseif strmatch(Program,'reorganize')
    out=arrangeHierarchy;
else
    [webTotal,resultPath]=makeH;
    output=cell2table(resultPath);
    output.Properties.VariableNames=webTotal';
    writetable(output,['C:\Users\neel\Box\My programs\Python\Django\','Pathway_out.xlsx'])
end
a=1

function [out]=arrangeHierarchy
% This code was used to convert all data to format that can be read using
% Postgres. This is used in the Django app
out={};
dir='C:\Users\neel\Box\My programs\Python\Django\';
f1=[dir, 'inputData.xlsx'];
web=table2cell(readtable(f1,'Sheet','Function_webH'));              % <--- change to Function_webH/Pathway_webH since this is what the sheet names are in the .xls file
dict=table2cell(readtable(f1,'Sheet','Fmember2web_dict'));          % <--- change to Fmember2web_dict/Pmember2web_dict
T=readtable(f1,'Sheet','Function_members');                         % <--- change to Function_members/Pathway_members
Theader=T.Properties.VariableNames;

key1=dict(:,1);
value1=dict(:,2);
M=containers.Map(key1,value1);
for k=1:length(Theader)
    idx=find(strcmp(Theader{k},key1));
    if ~isempty(idx)
        Theader{k}=M(key1{idx});
    end
end

members=table2cell(T);
ender=cell(size(web,1),1);  % This is the last term in a pathway series
temp='';
for i=1:size(web,1)
    ct=0;
    j=1;
    tempcell={};
    while (~isempty(web{i,j})||(ct==0))
        if isempty(char(web(i,j)))
            web{i,j}=web{i-1,j};
        else
            ct=1;
            temp=web{i,j};
        end
        j=j+1;
        if j>(size(web,2))
            break
        end
    end
    ender{i,1}=temp;
    idx=find(strcmp(Theader,temp));
    if isempty(idx)
        strcat(string(i),': ',temp)                             % this was used in the debugging step to ensure that the text fields are common between glycoEnzOnto and glycoEnzDB and to fix where not correct
    else
    memberI= members(:,idx);                                    % ith member
    memberI=memberI(~cellfun('isempty',memberI));               % remove empty elements of memberI
    tempcell=[repmat(web(i,:),size(memberI)),memberI];
    end
    out=[out;tempcell];
end
    NaNelements=cell2mat(cellfun(@(x) any(isnan(x)),out(:,end),'UniformOutput',false));
    out=out(~NaNelements,:);                                    % remove all rows with NaN---> this is what is used for webDisplay [out was copy pasted into excel instead of writing out an explicit file]
end

function  [webTotal,resultPath]=makeH
dir='C:\Users\neel\Box\My programs\Python\Django\';
f1=['C:\Users\neel\Box\My programs\Python\Django\', 'inputData.xlsx'];
f2=['C:\Users\neel\Box\My programs\Python\gnat\','finishedGlycogenes.xlsx'];
web=table2cell(readtable(f1,'Sheet','Pathway_webH'));           % <--- change to Function_webH/Pathway_webH
excel=table2cell(readtable(f2));
dictionary=table2cell(readtable(f1,'Sheet','Pathway_dict'));    % <--- change to Function_dict/Pathway_dict

% This reads dictionary file to get web-values (value1) for each excel-key (key1)
key1=dictionary(:,1);
value1=dictionary(:,2);
M=containers.Map(key1,value1);

% This reads the web file and links parent to children
for i=2:size(web,1)
    count=0;
    for j=1:size(web,2)
        if isempty(web{i,j}) && ~isempty(web{i-1,j}) && count==0
            web(i,j)=web(i-1,j);
        else
            count=1;
        end
    end
end
webTotal=unique(web);
webTotal(cellfun(@isempty,webTotal))=[]; % Find all members of web and get rid of empty cells

% populate resultPath [for Pathway]
gene=excel(:,2);
term=excel(:,6);                                            % <---This should be '6' for pathway and '7' for function
resultPath=cell(size(gene,1),size(webTotal,1));             % make empty result cell
counter=ones(size(webTotal,1),1);  % initalize counter
for i=1:length(term)
    cellX=strsplit(term{i},{',','|'},'CollapseDelimiters',true);
    cellX=strrep(cellX,' ','');                             % remove white space
    for j=1:size(cellX,2)
        if ~isempty(strmatch(cellX{j},key1,'exact'))
            val=M(cellX{j});
            child=getChildren(val,web);
            [val,':',child]
            for k=1:size(child,2)
                idx=strmatch(child(k),webTotal,'exact');
                if (counter(idx)==1)
                    resultPath(counter(idx),idx)=gene(i);
                    counter(idx)=counter(idx)+1;
                elseif isempty(strmatch(resultPath(counter(idx)-1,idx),gene(i),'exact'))
                    resultPath(counter(idx),idx)=gene(i);
                    counter(idx)=counter(idx)+1;
                end
            end
        else
            cellX{j}
            a=1;
        end
    end
end

% func=excel(i,7);
end

function child=getChildren(val,web)
child={'x'};
for i=1:size(web,1)
    temp=web(i,:);
    search=strsplit(val,',');
    if (size(search,2))==2
        if any(strcmp(search{2},temp))
            idx=strmatch(search{2},temp,'exact');
            if strmatch(temp(idx-1),search{1},'exact')
                child=temp(1:idx);
            end
        end
    else
        idx=strmatch(search{1},temp,'exact');
        if ~isempty(idx)
            child=temp(1:idx);
        end
    end
end
end


function out=getKeyValue(key)
% Find the unique Pathway or Function values in the excel sheet by removing
% duplictate entries
f2=['C:\Users\neel\Box\My programs\Python\gnat\','finishedGlycogenes.xlsx'];
excel=table2cell(readtable(f2));

if strcmp(key,'pathway')
    term=excel(:,6);   % pathway
else
    term=excel(:,7);   % function
end
cell1={};
pick='keep';
if strcmp(pick,'remove')
    for i=1:length(term)
        cell1=[cell1,strsplit(term{i},',')];
    end
    idx=cellfun(@(x) ~isempty(strfind(x,'|')), cell1, 'UniformOutput', false);  % remove cells that have '|'
    cell1(cell2mat(idx))=[];
else
    for i=1:length(term)
        cell1=[cell1,strsplit(term{i},{',','|'},'CollapseDelimiters',true)];
    end
end
cell1=strrep(cell1,' ','')  % remove white space
out=unique(cell1);
end