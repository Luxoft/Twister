/*
File: XMLBuilder.java ; This file is part of Twister.
Version: 3.004

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import com.twister.Item;
import com.twister.Configuration;
import java.util.ArrayList;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Text;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.OutputKeys;
import java.io.File;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.Result;
import java.io.FileInputStream;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import javax.swing.tree.DefaultMutableTreeNode;
import java.util.Scanner;
import java.util.HashMap;
import java.util.Iterator;
import java.util.ArrayList;


public class XMLBuilder{
    private DocumentBuilderFactory documentBuilderFactory;
    private Document document;
    private TransformerFactory transformerFactory;
    private Transformer transformer;
    private DOMSource source;
    private ArrayList <Item> suite;
    public boolean skip;
    private HashMap <String,ArrayList<String>> elements = new HashMap();//hash with initial id and list with final id's, if element was clone array contains multiple elements, first elem in array is first elem index
    private HashMap <Text,String> dependenciestags = new HashMap();//store dependecies tag and element first index+":"+ep

    public XMLBuilder(ArrayList <Item> suite){
        try{documentBuilderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            document = documentBuilder.newDocument();
            transformerFactory = TransformerFactory.newInstance();
            transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            source = new DOMSource(document);
            this.suite = suite;}
        catch(ParserConfigurationException e){
            System.out.println("DocumentBuilder cannot be created which satisfies the"+
                                " configuration requested");}
        catch(TransformerConfigurationException e){
            System.out.println("Could not create transformer");}}
        
    public boolean getRunning(Item item){
        if(item.getType()==1){
            if(item.getSubItem(0).getValue().equals("true")){
                return true;}
            else return false;}
        else{
            int subitemsnr = item.getSubItemsNr();
            for(int i=0;i<subitemsnr;i++){
                if(getRunning(item.getSubItem(i)))return true;}
            return false;}}
        
    public boolean createXML(boolean skip, boolean stoponfail,
                          boolean prestoponfail,
                          boolean temp, String prescript, String postscript,
                          boolean savedb, String delay, String[] globallibs,
                          String [][] projectdefined,String downloadlibraryoption
                          ){//skip checks if it is user or test xml
        int nrsuite = suite.size();
        Item current =null;
        if(!skip){
            //check for items without name
            for(int i=0;i<nrsuite;i++){
                current = RunnerRepository.hasEmptyName(suite.get(i));
                if(current!=null){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, RunnerRepository.window,"ERROR","There is an item with an empty name, please set name!");
                    return false;
                }
            }
        }
        this.skip = skip;
        Element root = document.createElement("Root");
        document.appendChild(root);
        Element em2 = document.createElement("stoponfail");
        if(stoponfail){
            em2.appendChild(document.createTextNode("true"));
        } else {
            em2.appendChild(document.createTextNode("false"));
        }
        root.appendChild(em2);
        em2 = document.createElement("PrePostMandatory");
        if(prestoponfail){
            em2.appendChild(document.createTextNode("true"));
        } else {
            em2.appendChild(document.createTextNode("false"));
        }
        if(projectdefined!=null&&projectdefined.length>0){
            for(int j=0;j<projectdefined.length;j++){
                Element userdef = document.createElement("UserDefined");
                Element pname = document.createElement("propName");
                pname.appendChild(document.createTextNode(projectdefined[j][0]));
                userdef.appendChild(pname);
                Element pvalue = document.createElement("propValue");
                pvalue.appendChild(document.createTextNode(projectdefined[j][1]));
                userdef.appendChild(pvalue);
                root.appendChild(userdef);}
        }
        root.appendChild(em2);
         em2 = document.createElement("DownloadLibraries");
         em2.appendChild(document.createTextNode(downloadlibraryoption));
         root.appendChild(em2);
        em2 = document.createElement("ScriptPre");
        em2.appendChild(document.createTextNode(prescript));
        root.appendChild(em2);
        em2 = document.createElement("ClearCaseView");
        em2.appendChild(document.createTextNode(ClearCase.getView()));
        root.appendChild(em2);
        em2 = document.createElement("libraries");
        StringBuilder sb = new StringBuilder();
        if(globallibs!=null){
            for(String s:globallibs){
                sb.append(s);
                sb.append(";");
            }
        }
        em2.appendChild(document.createTextNode(sb.toString()));
        root.appendChild(em2);
        
        
        em2 = document.createElement("ScriptPost");
        em2.appendChild(document.createTextNode(postscript));
        root.appendChild(em2);
        
        em2 = document.createElement("dbautosave");
        if(savedb){
            em2.appendChild(document.createTextNode("true"));
        } else {
            em2.appendChild(document.createTextNode("false"));
        }
        root.appendChild(em2);
        em2 = document.createElement("tcdelay");
        em2.appendChild(document.createTextNode(delay));
        root.appendChild(em2);
        if(skip && nrsuite>0){
            ArrayList <Item> temporary = new <Item> ArrayList();
            for(int i=0;i<nrsuite;i++){
                sb.setLength(0);
                current = suite.get(i);
                if(current.getEpId().length == 0){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, 
                                           RunnerRepository.window, "ERROR", 
                                           "Please set SUT for: "+current.getName());
                    return false;
                }
                for(String s:current.getEpId()){
                   DefaultMutableTreeNode noderoot =null;
                   String add = "";
                   if(s.indexOf("(user)")!=-1){
                       noderoot = RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().userroot;
                       s = s.replace("(user)", "");
                       add = ".user";
                   } else if(s.indexOf("(system)")!=-1){
                       noderoot = RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().globalroot;
                       s = s.replace("(system)", "");
                       add = ".system";
                   }
                   int sutsnr = noderoot.getChildCount();
                   for(int j=0;j<sutsnr;j++){
                       if(noderoot.getChildAt(j).toString().split(" - ")[0].equals(s)){
                           String eps = RunnerRepository.window.mainpanel.p4.getSut().sut.getEpsFromSut("/"+s+add);
                           for(String ep:eps.split(";")){
                               Item item = current.clone();
                               String []str = {ep,"/"+s+add};
                               item.setEpId(str);
                               temporary.add(item);
                           }
                       }
                   }
                }
             }
             suite = temporary;
             nrsuite = suite.size();
        }
        for(int i=0;i<nrsuite;i++){
            int nrtc = suite.get(i).getSubItemsNr();
            boolean go = false;
            if(!temp && skip){
                for(int j=0;j<nrtc;j++){
                    if(getRunning(suite.get(i))){
                        go=true;
                        break;}}}
            if(!go&&skip&&!temp)continue;
            Element rootElement = document.createElement("TestSuite");
            root.appendChild(rootElement);
            
            if(suite.get(i).getLibs()!=null&&suite.get(i).getLibs().length>0){
                em2 = document.createElement("libraries");
                sb.setLength(0);
                for(String s:suite.get(i).getLibs()){
                    sb.append(s);
                    sb.append(";");
                }
                em2.appendChild(document.createTextNode(sb.toString()));
                rootElement.appendChild(em2);
            }
            em2 = document.createElement("tsName");
            em2.appendChild(document.createTextNode(suite.get(i).getName()));
            rootElement.appendChild(em2);
            
            if(!skip){
                em2 = document.createElement("Repeat");
                em2.appendChild(document.createTextNode(suite.get(i).getRepeat()+""));
                rootElement.appendChild(em2);
            }
            
            
            em2 = document.createElement("PanicDetect");
            em2.appendChild(document.createTextNode(suite.get(i).isPanicdetect()+""));
            rootElement.appendChild(em2);
            
            sb = new StringBuilder();
            HashMap <Item,String> hash = suite.get(i).getDependencies();
            Iterator iter = hash.keySet().iterator();
            while(iter.hasNext()){
                Item elem = (Item)iter.next();
                sb.append(elem.getID());
                sb.append(":");
                sb.append(hash.get(elem));
                sb.append(";");
            }
            Element dependency = document.createElement("Dependency");
            Text text = document.createTextNode(sb.toString());
            dependency.appendChild(text);
            rootElement.appendChild(dependency);
            
            
            if(suite.get(i).getEpId()!=null&&suite.get(i).getEpId().length>0){
                em2 = document.createElement("ID");
                Text idtext = document.createTextNode(suite.get(i).getID());
                em2.appendChild(idtext);
                rootElement.appendChild(em2);
                
                if(skip){
                    Element EP = document.createElement("EpId");
                    String ep = suite.get(i).getEpId()[0];
                    try{
                        if(ep.equals("")){
                            System.out.print("Getting anonym ep for "+suite.get(i).getName());
                            ep=RunnerRepository.getRPCClient().execute("find_anonim_ep", new Object[]{RunnerRepository.user}).toString();
                            suite.get(i).setEpId(new String[]{ep,suite.get(i).getEpId()[1]});
                            System.out.println(" got ep: "+ep);
                        }
                    }
                    catch(Exception e){
                        System.out.println("Could not get EP from CE for:"+suite.get(i).getName());
                        e.printStackTrace();
                        return false;
                    }
                    if(ep.equalsIgnoreCase("false"))return false;
                    //dependenciestags.put(text, ep);
                    dependenciestags.put(text, suite.get(i).getPos().get(0).toString()+":"+ep);
                    idtext.setNodeValue(idtext.getNodeValue()+"#"+ep);//if testsuites.xml(skip) add ep to id
                    suite.get(i).setID(idtext.getNodeValue());
                    EP.appendChild(document.createTextNode(ep));
                    rootElement.appendChild(EP);
                    EP = document.createElement("SutName");
                    EP.appendChild(document.createTextNode(suite.get(i).getEpId()[1]));
                    rootElement.appendChild(EP);
                }
                else {
                    
                    StringBuilder b = new StringBuilder();
                    for(String s:suite.get(i).getEpId()){
                        b.append(s+";");
                    }
                    b.deleteCharAt(b.length()-1);
                    Element EP = document.createElement("SutName");
                    EP.appendChild(document.createTextNode(b.toString()));
                    rootElement.appendChild(EP);
                    EP = document.createElement("EpId");
                    b.setLength(0);
                    for(String s:suite.get(i).getEpId()){
                        DefaultMutableTreeNode noderoot =null;
                        String add = "";
                        if(s.indexOf("(user)")!=-1){
                            noderoot = RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().userroot;
                            s = s.replace("(user)", "");
                            add = ".user";
                        } else if(s.indexOf("(system)")!=-1){
                            noderoot = RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().globalroot;
                            s = s.replace("(system)", "");
                            add = ".system";
                        }
                        int sutsnr = 0;
                        if(noderoot!=null)sutsnr = noderoot.getChildCount();
                        for(int j=0;j<sutsnr;j++){
                            if(noderoot.getChildAt(j).toString().split(" - ")[0].equals(s)){
                                String eps = RunnerRepository.window.mainpanel.p4.getSut().sut.getEpsFromSut("/"+s+add);
                                b.append(eps);
                            }
                        }
                    }
                    if(b.length()>0)b.deleteCharAt(b.length()-1);
                    EP.appendChild(document.createTextNode(b.toString()));
                    rootElement.appendChild(EP);
                }
            } else {
                Element EP = document.createElement("EpId");
                rootElement.appendChild(EP);
                EP = document.createElement("SutName");
                rootElement.appendChild(EP);
            }
            for(int j=0;j<suite.get(i).getUserDefNr();j++){
                Element userdef = document.createElement("UserDefined");
                Element pname = document.createElement("propName");
                pname.appendChild(document.createTextNode(suite.get(i).getUserDef(j)[0]));
                userdef.appendChild(pname);
                Element pvalue = document.createElement("propValue");
                pvalue.appendChild(document.createTextNode(suite.get(i).getUserDef(j)[1]));
                userdef.appendChild(pvalue);
                rootElement.appendChild(userdef);}
            for(int j=0;j<nrtc;j++){
                addSubElement(suite.get(i),rootElement,suite.get(i).getSubItem(j),skip,temp);            
            }
        }
        if(skip){
            //map elements hash with the new ID's
            for(Item i:suite){
                populateElements(i);
            }
            sb = new StringBuilder();
            //assign final ids to dependecies saved with initialid
            for(Text tag:dependenciestags.keySet()){
                sb.setLength(0);
                String ep = dependenciestags.get(tag).split(":")[1];
                String index = dependenciestags.get(tag).split(":")[0];
                
                String[] dependencies = tag.getNodeValue().split(";");
                if(dependencies.length==0)continue;
                for(String dependency:dependencies){
                    if(dependency.length()==0)continue;
                    String status = dependency.split(":")[1];
                    String initialid = dependency.split(":")[0];
                    ArrayList <String> finalids = elements.get(initialid);                    
                    
                    if(finalids!=null&&finalids.size()>0){
                        if(finalids.size()==2){
                            sb.append(finalids.get(1));
                            sb.append(":");
                            sb.append(status);
                            sb.append(";");
                        } else {//if there are multiple id's element was cloned
                            boolean found = false;
                            int size = finalids.size();
                            if(finalids.get(0).equals(index)){//if they are on the same suite, insert only current ep dependency
                                sb.append(finalids.get(1).split("#")[0]);
                                sb.append("#");
                                sb.append(ep);
                                sb.append(":");
                                sb.append(status);
                                sb.append(";");
                            } else {//if they are not in  the same suite add all dependecies
                                for(int i=1;i<size;i++){
                                    String finalid = finalids.get(i);
                                    sb.append(finalid);
                                    sb.append(":");
                                    sb.append(status);
                                    sb.append(";");
                                }
                            }
                        }
                    }
                }
                tag.setNodeValue(sb.toString());
            }
        }
        return true;
    }
    
    private void populateElements(Item i){
        String initialid = i.getID().split("#")[0];
        ArrayList <String> idlist = elements.get(initialid);
        if(idlist==null){//if id not in elements create new one
            idlist = new ArrayList();
            idlist.add(i.getPos().get(0).toString());
            idlist.add(i.getID());
            elements.put(initialid, idlist);
        } else {//if element already exist, ad id to Array
            idlist.add(i.getID());
        }
        for(Item subitem:i.getSubItems()){
            populateElements(subitem);
        }
    }
                
    public void addSubElement(Item itemparent, Element rootelement, Item item, boolean skip, boolean temp){
        if(item.getType()==0){
            Element prop = document.createElement("Property");
            rootelement.appendChild(prop);
            Element em4 = document.createElement("propName");
            em4.appendChild(document.createTextNode(item.getName()));
            prop.appendChild(em4);
            Element em5 = document.createElement("propValue");
            em5.appendChild(document.createTextNode(item.getValue()));
            prop.appendChild(em5);}
        else if(item.getType()==1){
            if(!temp && item.getSubItem(0).getValue().equals("false") && skip)return;
            Element tc  = document.createElement("TestCase");
            rootelement.appendChild(tc);
            Element em3 = document.createElement("tcName");
            if(temp){
                em3.appendChild(document.createTextNode(item.getFileLocation()));
            }
            else{
                if(item.isClearcase()){
                    em3.appendChild(document.createTextNode(item.getFileLocation()));
                } else {
                    em3.appendChild(document.createTextNode(RunnerRepository.getTestSuitePath()+
                                        item.getFileLocation()));
                }
            }
            tc.appendChild(em3);
            
            if(!skip){
                em3 = document.createElement("Repeat");
                em3.appendChild(document.createTextNode(item.getRepeat()+""));  
                tc.appendChild(em3);
            }
            
            em3 = document.createElement("ID");
            Text idtext = document.createTextNode(item.getID());
            em3.appendChild(idtext);
            tc.appendChild(em3);
            
            
            
            StringBuilder sb = new StringBuilder();
            HashMap <Item,String> hash = item.getDependencies();
            Iterator iter = hash.keySet().iterator();
            while(iter.hasNext()){
                Item elem = (Item)iter.next();
                if(elem==null)continue;
                sb.append(elem.getID());
                sb.append(":");
                sb.append(hash.get(elem));
                sb.append(";");
            }
            Element dependency = document.createElement("Dependency");
            Text text = document.createTextNode(sb.toString());
            dependency.appendChild(text);
            tc.appendChild(dependency);
            
            if(skip){//if testsuites.xml add ep to id and dependency to hash
                idtext.setNodeValue(item.getID()+"#"+itemparent.getEpId()[0]);
                item.setID(item.getID()+"#"+itemparent.getEpId()[0]);
                //dependenciestags.put(text, itemparent.getEpId()[0]); 
                dependenciestags.put(text, itemparent.getPos().get(0).toString()+":"+itemparent.getEpId()[0]); 
            }
            
            if(item.isClearcase()){
                em3 = document.createElement("ClearCase");
                em3.appendChild(document.createTextNode("true"));
                tc.appendChild(em3);
            }
            em3 = document.createElement("ConfigFiles");
            
            Element em4 ;
            //sb = new StringBuilder();
            for(Configuration conf:item.getConfigurations()){
                em4 = document.createElement("Config");
                em4.setAttribute("name", conf.getFile());
                em4.setAttribute("enabled", conf.isEnabled()+"");
                em4.setAttribute("iterator_default", conf.isIeratorOD()+"");
                em4.setAttribute("iterator_sof", conf.isIteratorSOF()+"");
                em3.appendChild(em4);
                //sb.append(conf.getFile());
                //sb.append(";");
            }
//             for(String s:item.getConfigurations()){
//                 sb.append(s);
//                 sb.append(";");
//             }
//             if(sb.length()>0)sb.setLength(sb.length()-1);
//             em3.appendChild(document.createTextNode(sb.toString()));
            tc.appendChild(em3);
            if(temp || skip){
                Element em7 = document.createElement("Title");
                em7.appendChild(document.createTextNode(""));
                tc.appendChild(em7);
                Element em8 = document.createElement("Summary");
                em8.appendChild(document.createTextNode(""));
                tc.appendChild(em8);
                Element em9 = document.createElement("Priority");
                em9.appendChild(document.createTextNode("Medium"));
                tc.appendChild(em9);
            }
            if(item.isPrerequisite()){
                Element prop  = document.createElement("Property");
                tc.appendChild(prop);
                em4 = document.createElement("propName");
                em4.appendChild(document.createTextNode("setup_file"));
                prop.appendChild(em4);
                Element em5 = document.createElement("propValue");
                em5.appendChild(document.createTextNode("true"));
                prop.appendChild(em5);}
            if(item.isTeardown()){
                Element prop  = document.createElement("Property");
                tc.appendChild(prop);
                em4 = document.createElement("propName");
                em4.appendChild(document.createTextNode("teardown_file"));
                prop.appendChild(em4);
                Element em5 = document.createElement("propValue");
                em5.appendChild(document.createTextNode("true"));
                prop.appendChild(em5);}
            if(item.isOptional()){
                Element prop  = document.createElement("Property");
                tc.appendChild(prop);
                em4 = document.createElement("propName");
                em4.appendChild(document.createTextNode("Optional"));
                prop.appendChild(em4);
                Element em5 = document.createElement("propValue");
                em5.appendChild(document.createTextNode("true"));
                prop.appendChild(em5);}
            Element prop  = document.createElement("Property");
            tc.appendChild(prop);
            em4 = document.createElement("propName");
            em4.appendChild(document.createTextNode("Runnable"));
            prop.appendChild(em4);
            Element em5 = document.createElement("propValue");
            em5.appendChild(document.createTextNode(item.isRunnable()+""));
            prop.appendChild(em5);
            int nrprop = item.getSubItemsNr();
            int k=0;
            if(!temp && skip)k=1;
            for(;k<nrprop;k++)addSubElement(item,tc,item.getSubItem(k),skip,temp);}
        else{int nrtc = item.getSubItemsNr();
            boolean go = false;
            if(!temp && skip){
                for(int j=0;j<nrtc;j++){
                    if(getRunning(item.getSubItem(j))){
                        go=true;
                        break;}}}
            if(!go&&skip&&!temp)return;
            Element rootElement2 = document.createElement("TestSuite");
            rootelement.appendChild(rootElement2);
            Element em2 = document.createElement("tsName");
            em2.appendChild(document.createTextNode(item.getName()));
            rootElement2.appendChild(em2);
            if(!skip){
                em2 = document.createElement("Repeat");
                em2.appendChild(document.createTextNode(item.getRepeat()+""));
                rootElement2.appendChild(em2);
            }
            
            em2 = document.createElement("ID");
            Text idtext = document.createTextNode(item.getID());
            em2.appendChild(idtext);
            rootElement2.appendChild(em2);
            
            StringBuilder sb = new StringBuilder();
            HashMap <Item,String> hash = item.getDependencies();
            Iterator iter = hash.keySet().iterator();
            while(iter.hasNext()){
                Item elem = (Item)iter.next();
                sb.append(elem.getID());
                sb.append(":");
                sb.append(hash.get(elem));
                sb.append(";");
            }
            Element dependency = document.createElement("Dependency");
            Text text = document.createTextNode(sb.toString());
            dependency.appendChild(text);
            rootElement2.appendChild(dependency);
            
            if(item.getEpId()!=null&&!item.getEpId().equals("")){                
                if(skip){
                    Element EP = document.createElement("EpId");                    
                    EP.appendChild(document.createTextNode(item.getEpId()[0]));
                    rootElement2.appendChild(EP);                    
                    EP = document.createElement("SutName");
                    EP.appendChild(document.createTextNode(item.getEpId()[1]));
                    rootElement2.appendChild(EP);
                    //dependenciestags.put(text, item.getEpId()[0]); 
                    dependenciestags.put(text, item.getPos().get(0).toString()+":"+item.getEpId()[0]);
                    idtext.setNodeValue(idtext.getNodeValue()+"#"+item.getEpId()[0]);
                    item.setID(idtext.getNodeValue()+"#"+item.getEpId()[0]);
                } else {
                    Element EP = document.createElement("SutName");
                    StringBuilder b = new StringBuilder();
                    for(String s:item.getEpId()){
                        b.append(s+";");
                    }
                    b.deleteCharAt(b.length()-1);                   
                    EP.appendChild(document.createTextNode(b.toString()));
                    rootElement2.appendChild(EP);
                    EP = document.createElement("EpId");
                    b.setLength(0);
                    DefaultMutableTreeNode noderoot =null;
                    for(String s:item.getEpId()){
                        String add = "";
                        if(s.indexOf("(user)")!=-1){
                            noderoot = RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().userroot;
                            s = s.replace("(user)", "");
                            add = ".user";
                        } else if(s.indexOf("(system)")!=-1){
                            noderoot = RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().globalroot;
                            s = s.replace("(system)", "");
                            add = ".system";
                        }
                        int sutsnr = noderoot.getChildCount();                        
                        for(int j=0;j<sutsnr;j++){
                            if(noderoot.getChildAt(j).toString().split(" - ")[0].equals(s)){
                                String eps = RunnerRepository.window.mainpanel.p4.getSut().sut.getEpsFromSut("/"+s+add);
                                b.append(eps);
                            }
                        }
                    }
                    EP.appendChild(document.createTextNode(b.toString()));
                    rootElement2.appendChild(EP);                    
                }
                //temporary solution for CE
                if(skip){
                    Item parent = suite.get(item.getPos().get(0));            
                    for(int j=0;j<parent.getUserDefNr();j++){
                        Element userdef = document.createElement("UserDefined");
                        Element pname = document.createElement("propName");
                        pname.appendChild(document.createTextNode(parent.getUserDef(j)[0]));
                        userdef.appendChild(pname);
                        Element pvalue = document.createElement("propValue");
                        pvalue.appendChild(document.createTextNode(parent.getUserDef(j)[1]));
                        userdef.appendChild(pvalue);
                        rootElement2.appendChild(userdef);}
                }
                //end solution for CE
            }
            for(int i=0;i<item.getSubItemsNr();i++){
                addSubElement(item,rootElement2,item.getSubItem(i),skip,temp);
            }}}     
            
    public void printXML(){        
        StreamResult result =  new StreamResult(System.out);
        try{transformer.transform(source, result);}
        catch(Exception e){System.out.println("Could not write standard output stream");}}
        
        
    public boolean writeXMLFile(String filename, boolean local, boolean temp, boolean lib){
        File file = new File(filename);
        if(temp)file = new File(RunnerRepository.temp +RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+ filename);
        Result result = new StreamResult(file);
        try{transformer.transform(source, result);}
        catch(Exception e){
            e.printStackTrace();
            System.out.println("Could not write to file: "+file.getAbsolutePath());
            return false;}
        if(!local){
            try{
                if(temp || skip){//testsuites.xml
                    String dir = RunnerRepository.getXMLRemoteDir();
                    String [] path = dir.split("/");
                    StringBuffer result2 = new StringBuffer();
                    if (path.length > 0){
                        for (int i=0; i<path.length-1; i++){
                            result2.append(path[i]);
                            result2.append("/");}}
                    FileInputStream in = new FileInputStream(file);
                    return RunnerRepository.uploadRemoteFile(result2.toString(), in,null, file.getName(),false,null);
                }else{
                    if(lib){ //predefined suites  
                        return RunnerRepository.savePredefinedProjectFile(RunnerRepository.getPredefinedSuitesPath()+"/"+file.getName(),new Scanner(file).useDelimiter("\\A").next());
                    } else {//normal suites                        
                        if(RunnerRepository.saveProjectFile(file.getName(),new Scanner(file).useDelimiter("\\A").next())==null){
                            return false;
                        }
                        return true;
                    }
                }}
            catch(Exception e){e.printStackTrace();
                System.out.println("Could not get XML file to upload on sever");
                return false;}}
        return true;}}
