/*
File: XMLReader.java ; This file is part of Twister.
Version: 2.028

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
import java.io.File;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;
import java.io.IOException;
import java.awt.Graphics;
import java.awt.FontMetrics;
import java.awt.Font;
import java.util.ArrayList;
import java.util.HashMap;
import com.twister.Configuration;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;

public class XMLReader{
    private int preprop = 12;//properties in xml available before Property tag, in testsuites repeat tag is not present, we will substract 2
    private Document doc;
    private Element fstNmElmnt,
                    secNmElmnt,trdNmElmnt;
    private NodeList fstNmElmntLst,fstNm,secNmElmntLst,secNm,
                     trdNmElmntLst,trdNm,trdNmElmntLst2,trdNm2;
    private File f;
    private String name,value;
    private int index = 1001;
    private HashMap <String, Item> projectitems;
    private HashMap <Item, String> dependencies;
    private boolean mismatchshown;
    
    
    public XMLReader (File file){
        dependencies = new HashMap();
        projectitems = new HashMap();
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = null;
        try{db = dbf.newDocumentBuilder();}
        catch(ParserConfigurationException e){
            System.out.println("Could not create a XML parser configuration");}
        try{doc = db.parse(file);}
        catch(SAXException e){
            try{System.out.println("The document"+file.getCanonicalPath()+
                                    " is empty or not valid");}
            catch(Exception ex){e.printStackTrace();}}
        catch(IOException e){
            try{System.out.println("Could not read the document"+
                                    file.getCanonicalPath());}
            catch(Exception ex){e.printStackTrace();}}
        try{doc.getDocumentElement().normalize();}
        catch(Exception e){e.printStackTrace();}}
        
    public void manageSubChilderen(Item item,Node node,ArrayList <Integer> indexes,
                                    Graphics g, boolean test){
        if(!node.getNodeName().equals("Property")){
            Item theone;
            int k = 0;
            if(node.getNodeName().equals("TestSuite")){
                fstNmElmntLst = ((Element)node).getElementsByTagName("tsName");
                fstNmElmnt = (Element)fstNmElmntLst.item(0);
                fstNm = fstNmElmnt.getChildNodes();
                FontMetrics metrics = g.getFontMetrics(new Font("TimesRoman", 1, 13));
                int width = metrics.stringWidth(fstNm.item(0).getNodeValue().toString());
                
                if(test){
                    theone = new Item(fstNm.item(0).getNodeValue(),2,
                                        -1,10, width+120,25,indexes);}
                else{
                    theone = new Item(fstNm.item(0).getNodeValue(),2,
                                        -1,10, width+50,25,indexes);}
                                        
                fstNmElmntLst = ((Element)node).getElementsByTagName("ID");
                if(fstNmElmntLst.getLength()>0){
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    theone.setID(fstNm.item(0).getNodeValue().toString());
                    projectitems.put(theone.getID(), theone);
                }
                
                fstNmElmntLst = ((Element)node).getElementsByTagName("Dependency");
                if(fstNmElmntLst.getLength()>0){
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    if(fstNm.getLength()>0)dependencies.put(theone, fstNm.item(0).getNodeValue().toString());
                } else if(!RunnerRepository.isMaster()){//this is not master
                    if(!test){
                        preprop -=2;
                    }
                }
                fstNmElmntLst = ((Element)node).getElementsByTagName("Repeat");
                if(fstNmElmntLst.getLength()>0){
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    if(fstNm.getLength()>0)theone.setRepeat(Integer.parseInt(fstNm.item(0).getNodeValue().toString()));
                    if(theone.getRepeat()>1){
                        width = metrics.stringWidth(theone.getRepeat()+"X "+theone.getName())+40;
                        theone.getRectangle().setSize(width,(int)theone.getRectangle().getHeight());
                    }
                }
                
                
                if(test){
                    String []text={""};
                    try{                          
                        fstNmElmntLst = ((Element)node).getElementsByTagName("EpId");
                        fstNmElmnt = (Element)fstNmElmntLst.item(0);
                        fstNm = fstNmElmnt.getChildNodes();
                        text[0] = fstNm.item(0).getNodeValue()+" : ";
                    } catch(Exception e){ e.printStackTrace();}
                    try{                          
                        fstNmElmntLst = ((Element)node).getElementsByTagName("SutName");
                        fstNmElmnt = (Element)fstNmElmntLst.item(0);
                        fstNm = fstNmElmnt.getChildNodes();
                        String sut = fstNm.item(0).getNodeValue();
                        sut = sut.replace(".system","(system)");
                        sut = sut.replace(".user","(user)");
                        sut = sut.substring(1);
                        text[0] += sut;
                    } catch(Exception e){ e.printStackTrace();}
                    theone.setEpId(text);
                } else{
                        try{
                            fstNmElmntLst = ((Element)node).getElementsByTagName("SutName");
                            fstNmElmnt = (Element)fstNmElmntLst.item(0);
                            fstNm = fstNmElmnt.getChildNodes();
                        } catch(Exception ex){
                            System.out.println("Could not find EpId/SutName tag");
                            ex.printStackTrace();
                        }
                    theone.setEpId(fstNm.item(0).getNodeValue().split(";"));
                }
                
                //temporary solution for CE
                if(test){
                   try{
                       k=preprop;
                       NodeList list = ((Element)node).getChildNodes();
                       for(int i=0;i<list.getLength();i++){
                           if(list.item(i).getNodeName().equals("UserDefined")){
                               k+=2;
                            }
                        }
                    } catch(Exception e){
                        e.printStackTrace();
                        k=preprop;
                    } 
                } else {
                    if(RunnerRepository.isMaster())k=preprop;    
                    else k=preprop-2;
                }
                //temporary solution for CE
            }
            else{
                secNmElmntLst = ((Element)node).getElementsByTagName("tcName");
                if(secNmElmntLst.getLength()==0)return;
                secNmElmnt = (Element)secNmElmntLst.item(0);
                secNm = secNmElmnt.getChildNodes();
                FontMetrics metrics = g.getFontMetrics(new Font("TimesRoman", 0, 13));
                NodeList clearcase = ((Element)node).getElementsByTagName("ClearCase");
                String f = "";
                boolean isclearcase = false;
                if(clearcase.getLength()==0){
                    try{f = secNm.item(0).getNodeValue().toString().
                            split(RunnerRepository.getTestSuitePath())[1];}
                    catch(Exception e){
                        if(!mismatchshown){
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,RunnerRepository.window,
                                                "Error", "It looks like there is a mismatch between suitespath and test cases in project!");
                            mismatchshown = true;
                        }
                        System.out.println("Could not split: "+secNm.item(0).getNodeValue().toString()+" with: "+RunnerRepository.getTestSuitePath()+". Maybe there is a diffenrent suitepath defined in project.");
                        e.printStackTrace();
                        f = secNm.item(0).getNodeValue().toString();
                    }
                    k=2;
//                     k=6;
                } else {
                    f = secNm.item(0).getNodeValue().toString();
                    isclearcase = true;
                    k=4;
//                     k=8;
                }
                
                int width = metrics.stringWidth(f) + 8;
                if(test){f = secNm.item(0).getNodeValue().toString();}   
                theone = new Item(f,1,-1,-1,width+40,20,indexes);
                theone.setClearcase(isclearcase);
                theone.setCEindex(index++);
                
                
                secNmElmntLst = ((Element)node).getElementsByTagName("ID");
                if(secNmElmntLst.getLength()!=0){
                    secNmElmnt = (Element)secNmElmntLst.item(0);
                    secNm = secNmElmnt.getChildNodes();
                    theone.setID(secNm.item(0).getNodeValue().toString());
                    projectitems.put(theone.getID(), theone);
                }
                
                fstNmElmntLst = ((Element)node).getElementsByTagName("Dependency");
                if(fstNmElmntLst.getLength()>0){
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    if(fstNm.getLength()>0)dependencies.put(theone, fstNm.item(0).getNodeValue().toString());
                }
                
                fstNmElmntLst = ((Element)node).getElementsByTagName("Repeat");
                if(fstNmElmntLst.getLength()>0){
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    if(fstNm.getLength()>0)theone.setRepeat(Integer.parseInt(fstNm.item(0).getNodeValue().toString()));
                    if(theone.getRepeat()>1){
                        width = metrics.stringWidth(theone.getRepeat()+"X "+theone.getName())+40;
                        theone.getRectangle().setSize(width,(int)theone.getRectangle().getHeight());
                    }
                }
                
                secNmElmntLst = ((Element)node).getElementsByTagName("ConfigFiles");
                if(secNmElmntLst.getLength()>0){
                    secNmElmnt = (Element)secNmElmntLst.item(0);
                    //secNm = secNmElmnt.getChildNodes();
                    
                    secNmElmntLst = ((Element)node).getElementsByTagName("Config");
                    int size = secNmElmntLst.getLength();
                    if(size>0){
                        for(int i=0;i<size;i++){
                            Element em = (Element)secNmElmntLst.item(i);
                            Configuration conf = new Configuration(em.getAttribute("name"));
                            conf.setEnabled(Boolean.parseBoolean(em.getAttribute("enabled")));
                            conf.setIeratorOD(Boolean.parseBoolean(em.getAttribute("iterator_default")));
                            conf.setIteratorSOF(Boolean.parseBoolean(em.getAttribute("iterator_sof")));
                            theone.getConfigurations().add(conf);
                        }
                    }
                    
                    
                    //String configs[] ={};
//                     if(secNm.getLength()>0){
//                         configs = secNm.item(0).getNodeValue().toString().split(";");
//                         for(String conf:configs){
//                             theone.getConfigurations().add(new Configuration(conf));
//                         }
//                     }
                    //theone.setConfigurations(configs);
                    k+=2;
                }
                if(test){
                    ArrayList <Integer> indexpos3 = (ArrayList <Integer>)indexes.clone();
                    indexpos3.add(new Integer(0));
                    name = "Status";
                    value = "Pending";
                    metrics = g.getFontMetrics(new Font("TimesRoman", 0, 11));
                    width = metrics.stringWidth(name+":  "+value) + 8;
                    Item property = new Item(name,0,-1,-1,width+20,20,indexpos3);
                    property.setSubItemVisible(true);
                    property.setValue(value);
                    theone.addSubItem(property);}
                else{
                    ArrayList <Integer> indexpos3 = (ArrayList <Integer>)indexes.clone();
                    indexpos3.add(new Integer(0));
                    name = "Running";
                    value = "true";
                    metrics = g.getFontMetrics(new Font("TimesRoman", 0, 11));
                    width = metrics.stringWidth(name+":  "+value) + 8;
                    Item property = new Item(name,0,-1,-1,width+20,20,indexpos3);
                    property.setSubItemVisible(false);
                    property.setValue(value);
                    theone.addSubItem(property);}
            }
//            if(!(test&&theone.getType()==1)){//if it is test the props should not be read further
                int subchildren = node.getChildNodes().getLength();
                int index=0;
                for(;k<subchildren-1;k++){
                    ArrayList <Integer> temp = (ArrayList <Integer>)indexes.clone();
                    temp.add(new Integer(index));
                    k++;
                    manageSubChilderen(theone,node.getChildNodes().item(k),temp,g,test);
                    index++;}
//                 }
            item.addSubItem(theone);}
        else{
            trdNmElmntLst = ((Element)node).getElementsByTagName("propName");
            trdNmElmnt = (Element)trdNmElmntLst.item(0);
            trdNm = trdNmElmnt.getChildNodes();
            if(trdNm.getLength()>0)name = trdNm.item(0).getNodeValue().toString();
            else name = "";
            if(name.equals("Runnable")){
                trdNmElmntLst2 = ((Element)node).getElementsByTagName("propValue");
                Element trdNmElmnt2 = (Element)trdNmElmntLst2.item(0);
                trdNm2 = trdNmElmnt2.getChildNodes();
                value = trdNm2.item(0).getNodeValue().toString();
                item.setRunnable(Boolean.parseBoolean(value));
                return;}
            else if(name.equals("teardown_file")){
                item.setTeardown(true);
                return;}
            else if(name.equals("setup_file")){
                item.setPrerequisite(true);
                return;}
            else if(name.equals("Optional")){
                item.setOptional(true);
                return;}
            trdNmElmntLst2 = ((Element)node).getElementsByTagName("propValue");
            Element trdNmElmnt2 = (Element)trdNmElmntLst2.item(0);
            trdNm2 = trdNmElmnt2.getChildNodes();
            if(trdNm2.getLength()>0)value = trdNm2.item(0).getNodeValue().toString();
            else value = "";
            if(name.equals("Running")){
                item.setCheck(Boolean.parseBoolean(value),true);
                return;
            }
            FontMetrics metrics = g.getFontMetrics(new Font("TimesRoman", 0, 11));
            int width = metrics.stringWidth(name+":  "+value) + 8;
            indexes.set(indexes.size()-1,
                        new Integer(indexes.get(indexes.size()-1).intValue()-1));
            int index = item.getSubItemsNr();
            indexes.set(indexes.size()-1, index);
            Item property = new Item(name,0,-1,-1,width+30,20,indexes);
            property.setSubItemVisible(false);
            property.setValue(value);
            item.addSubItem(property);
            item.setVisible(false);
        }
    }
    
    /*
     * clear - if the parser populates a custom array it should be false
     * clear is true when opening a new file in Repositor array
     */    
    public void parseXML(Graphics g,boolean test,ArrayList <Item> suite, boolean clear){
        if(!test&&clear){
            RunnerRepository.window.mainpanel.p1.suitaDetails.setGlobalLibs(null);
            RunnerRepository.window.mainpanel.p1.suitaDetails.setSaveDB("None");
            RunnerRepository.window.mainpanel.p1.suitaDetails.setDelay("");
            RunnerRepository.window.mainpanel.p1.suitaDetails.setStopOnFail(false);
            RunnerRepository.window.mainpanel.p1.suitaDetails.setPreStopOnFail(false);
            RunnerRepository.window.mainpanel.p1.suitaDetails.setPostScript("");
            RunnerRepository.window.mainpanel.p1.suitaDetails.setPreScript("");
            if(RunnerRepository.isMaster()){
                RunnerRepository.window.mainpanel.p1.suitaDetails.setGlobalDownloadType(null);
            }
        }
        if(test)preprop-=2;//in testsuites repeat tag is not present
        mismatchshown = false;
        NodeList nodeLst = doc.getChildNodes().item(0).getChildNodes();
        int childsnr = doc.getChildNodes().item(0).getChildNodes().getLength();
        if(childsnr==0){
            try{System.out.println(f.getCanonicalPath()+" has no content");}
            catch(Exception e){e.printStackTrace();}}
        int indexsuita = 0;
        ArrayList<String[]> userDefined = new ArrayList<String[]>();
        for(int m=0;m<childsnr;m++){
            Node fstNode = nodeLst.item(m);
            if(!test&&clear){
                if(fstNode.getNodeName().equals("stoponfail")){
                    if(fstNode.getChildNodes().item(0).getNodeValue().toString().equals("true")){                    
                        RunnerRepository.window.mainpanel.p1.suitaDetails.setStopOnFail(true);
                    }
                    else RunnerRepository.window.mainpanel.p1.suitaDetails.setStopOnFail(false);
                    continue;
                }
                else if(fstNode.getNodeName().equals("PrePostMandatory")){
                    if(fstNode.getChildNodes().item(0).getNodeValue().toString().equals("true")){                    
                        RunnerRepository.window.mainpanel.p1.suitaDetails.setPreStopOnFail(true);
                    }
                    else RunnerRepository.window.mainpanel.p1.suitaDetails.setPreStopOnFail(false);
                    continue;
                }
                else if(fstNode.getNodeName().equals("tcdelay")){
                    String delay = "";
                    try{delay = fstNode.getChildNodes().item(0).getNodeValue().toString();}
                    catch(Exception e){
                        delay = "";
                    }
                    RunnerRepository.window.mainpanel.p1.suitaDetails.setDelay(delay);
                    continue;
                }
                else if(fstNode.getNodeName().equals("dbautosave")){                  
                    try{RunnerRepository.window.mainpanel.p1.suitaDetails.setSaveDB(fstNode.getChildNodes().item(0).getNodeValue().toString());}
                    catch(Exception e){
                        System.out.println("dbautosave tag in project is not set");
                        RunnerRepository.window.mainpanel.p1.suitaDetails.setSaveDB("null");
                    }
                    continue;
                }
                else if(fstNode.getNodeName().equals("ScriptPre")){
                    String script = "";
                    try{script = fstNode.getChildNodes().item(0).getNodeValue().toString();}
                    catch(Exception e){script = "";}
                    RunnerRepository.window.mainpanel.p1.suitaDetails.setPreScript(script);
                    continue;
                }
                else if(fstNode.getNodeName().equals("ClearCaseView")){
                    try{
                        String view = fstNode.getChildNodes().item(0).getNodeValue().toString();
                        ClearCase.setView(view);}
                    catch(Exception e){
                        ClearCase.setView("");
                    }
                    continue;
                }
                else if(fstNode.getNodeName().equals("DownloadLibraries")){
                    if(RunnerRepository.isMaster()){
                        try{String librarydownloadtype = fstNode.getChildNodes().item(0).getNodeValue().toString();
                            RunnerRepository.window.mainpanel.p1.suitaDetails.setGlobalDownloadType(librarydownloadtype);}
                        catch(Exception e){
                            RunnerRepository.window.mainpanel.p1.suitaDetails.setGlobalDownloadType(null);
                        }
                        continue;
                    }
                }
                else if(fstNode.getNodeName().equals("ScriptPost")){
                    String script = "";
                    try{script = fstNode.getChildNodes().item(0).getNodeValue().toString();}
                    catch(Exception e){script = "";}
                    RunnerRepository.window.mainpanel.p1.suitaDetails.setPostScript(script);
                    continue;
                }
                else if(fstNode.getNodeName().equals("libraries")){
                    String [] libraries = {};
                    try{libraries = fstNode.getChildNodes().item(0).getNodeValue().toString().split(";");}
                    catch(Exception e){libraries = new String[]{};}
                    RunnerRepository.window.mainpanel.p1.suitaDetails.setGlobalLibs(libraries);
                    continue;
                } else if(fstNode.getNodeName().equals("UserDefined")){
                    try{
                        Element element = (Element)fstNode;                
                        NodeList propname = element.getElementsByTagName("propName");
                        Element el1 = (Element)propname.item(0);
                        fstNm = el1.getChildNodes();
                        String prop ;
                        if(fstNm.getLength()>0)prop= fstNm.item(0).getNodeValue();
                        else prop = "";
                        
                        NodeList propvalue = element.getElementsByTagName("propValue");
                        Element el2 = (Element)propvalue.item(0);
                        fstNm = el2.getChildNodes();
                        String val ;
                        if(fstNm.getLength()>0)val = fstNm.item(0).getNodeValue();
                        else val = "";
                        String add [] = {prop,val};
                        userDefined.add(add);
                    }
                    catch(Exception e){
                        System.out.println("There was a problem in reading propName,propValue and add to userDefined");
                    }
                    continue;
                }
            }
            if(!fstNode.getNodeName().equals("TestSuite"))continue;            
            ArrayList <Integer> indexpos = new ArrayList <Integer> ();
            indexpos.add(new Integer(indexsuita));            
            Element fstElmnt = (Element)fstNode;
            fstNmElmntLst = fstElmnt.getElementsByTagName("tsName");
            fstNmElmnt = (Element)fstNmElmntLst.item(0);
            fstNm = fstNmElmnt.getChildNodes();
            FontMetrics metrics = g.getFontMetrics(new Font("TimesRoman", 1, 13));
            String name = "";
            try{name = fstNm.item(0).getNodeValue().toString();}
            catch(Exception e){System.out.println("There is a suite with no name in project");}
            int width = metrics.stringWidth(name);
            Item suitatemp;
            if(!test)suitatemp= new Item(name,
                                         2,-1,10, width+50,25,indexpos);
            else suitatemp=  new Item(name,
                                      2,-1,10, width+120,25,indexpos);
            int k=preprop;            
            fstNmElmntLst = fstElmnt.getElementsByTagName("libraries");
            if(fstNmElmntLst.getLength()>0){
                fstNmElmnt = (Element)fstNmElmntLst.item(0);
                fstNm = fstNmElmnt.getChildNodes();
                if(fstNm.getLength()>0){
                    suitatemp.setLibs(fstNm.item(0).getNodeValue().split(";"));
                }
                k+=2;
            }
            fstNmElmntLst = fstElmnt.getElementsByTagName("ID");
            if(fstNmElmntLst.getLength()>0){
                fstNmElmnt = (Element)fstNmElmntLst.item(0);
                fstNm = fstNmElmnt.getChildNodes();
                suitatemp.setID(fstNm.item(0).getNodeValue());
                projectitems.put(suitatemp.getID(), suitatemp);
            } else {
                if(!test)k-=2;
            }
            
            fstNmElmntLst = fstElmnt.getElementsByTagName("Dependency");
            if(fstNmElmntLst.getLength()>0){
                fstNmElmnt = (Element)fstNmElmntLst.item(0);
                fstNm = fstNmElmnt.getChildNodes();
                if(fstNm.getLength()>0)dependencies.put(suitatemp, fstNm.item(0).getNodeValue().toString());
            }else {
                if(!test)k-=2;
            }
            
            fstNmElmntLst = fstElmnt.getElementsByTagName("Repeat");
            if(fstNmElmntLst.getLength()>0){
                fstNmElmnt = (Element)fstNmElmntLst.item(0);
                fstNm = fstNmElmnt.getChildNodes();
                if(fstNm.getLength()>0)suitatemp.setRepeat(Integer.parseInt(fstNm.item(0).getNodeValue().toString()));
                if(suitatemp.getRepeat()>1){
                    width = metrics.stringWidth(suitatemp.getRepeat()+"X "+suitatemp.getName())+40;
                    suitatemp.getRectangle().setSize(width,(int)suitatemp.getRectangle().getHeight());
                }
            }else {
                if(!test)k-=2;
            }
            
            try{fstNmElmntLst = fstElmnt.getElementsByTagName("PanicDetect");
                if(fstNmElmntLst.getLength()>0){
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    suitatemp.setPanicdetect(Boolean.parseBoolean(fstNm.item(0).getNodeValue()));
                    k+=2;
                }
            } catch(Exception e){
                e.printStackTrace();
            }
            if(test){
                String []text={""};
                try{                          
                    fstNmElmntLst = fstElmnt.getElementsByTagName("EpId");
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    text[0] = fstNm.item(0).getNodeValue()+" : ";
                } catch(Exception e){ e.printStackTrace();}
                try{                          
                    fstNmElmntLst = fstElmnt.getElementsByTagName("SutName");
                    fstNmElmnt = (Element)fstNmElmntLst.item(0);
                    fstNm = fstNmElmnt.getChildNodes();
                    String sut = fstNm.item(0).getNodeValue();
                    sut = sut.replace(".system","(system)");
                    sut = sut.replace(".user","(user)");
                    sut = sut.substring(1);
                    text[0] += sut;
                } catch(Exception e){ e.printStackTrace();}
                suitatemp.setEpId(text);
            } else{                
                try{fstNmElmntLst = fstElmnt.getElementsByTagName("SutName");
                    if(fstNmElmntLst.getLength()>0){
                        fstNmElmnt = (Element)fstNmElmntLst.item(0);
                        fstNm = fstNmElmnt.getChildNodes();
                    } else {
                        System.out.println("There is an element that has no EpId or SutName!!!");
                    }
                } catch (Exception ex){
                    
                    ex.printStackTrace();
                }
                try{suitatemp.setEpId(fstNm.item(0).getNodeValue().split(";"));}
                catch(Exception e){
                    if(fstNm.item(0)!=null){
                        String [] s = {fstNm.item(0).getNodeValue()};
                        suitatemp.setEpId(s);
                    } else {
                        suitatemp.setEpId(new String[]{});
                    }
                }
            }
            
            //temp solution for CE
            int items = fstElmnt.getChildNodes().getLength();
            int userdefinitions = 0;
            for(int i=0;i<items;i++){
                if(fstElmnt.getChildNodes().item(i).getNodeName().equals("UserDefined"))userdefinitions++;
            }
            for(int i=0;i<items;i++){
                if(fstElmnt.getChildNodes().item(i).getNodeName().equals("UserDefined")){
                    Element element = (Element)fstElmnt.getChildNodes().item(i);                
                    NodeList propname = element.getElementsByTagName("propName");
                    Element el1 = (Element)propname.item(0);
                    fstNm = el1.getChildNodes();
                    String prop ;
                    if(fstNm.getLength()>0)prop= fstNm.item(0).getNodeValue();
                    else prop = "";
                    NodeList propvalue = element.getElementsByTagName("propValue");
                    Element el2 = (Element)propvalue.item(0);
                    fstNm = el2.getChildNodes();
                    String val ;
                    if(fstNm.getLength()>0)val = fstNm.item(0).getNodeValue();
                    else val = "";
                    suitatemp.addUserDef(new String[]{prop,val});
                }
            }
            //temp solution for CE                
                
                
            int subchildren = fstElmnt.getChildNodes().getLength();
            int index=0;
            indexsuita++;
            for( k+=userdefinitions*2;k<subchildren-1;k++){
                k++;
                ArrayList <Integer> temp =(ArrayList <Integer>)indexpos.clone();
                temp.add(new Integer(index));
                manageSubChilderen(suitatemp,fstElmnt.getChildNodes().item(k),
                                    temp,g,test);
                index++;}
            if(!test)suite.add(suitatemp);
            else{
                suite.add(suitatemp);
                
                String currents = suitatemp.getEpId()[0].split(" : ")[0];
                    boolean found = false;
                    for(String s:RunnerRepository.getLogs()){
                        if(s.equals(currents+"_"+RunnerRepository.getLogs().get(4))){                        
                            found = true;
                            break;
                        }                    
                    }
                    if(!found){
                            RunnerRepository.getLogs().add(currents+"_"+
                                                     RunnerRepository.getLogs().get(4));
                    }
                }
            }
        int size = RunnerRepository.window.mainpanel.p1.suitaDetails.getProjectDefsNr();
        if(userDefined.size()!=size){
            System.out.println("Warning, project has "+userDefined.size()+" fields while in db.xml are defined "+size+" fields");
        }
        RunnerRepository.window.mainpanel.p1.suitaDetails.setProjectUserDefined(userDefined);
        //manage defined dependencie
        for(Item item:dependencies.keySet()){
            String values = dependencies.get(item);
            String dependencie [] = values.split(";");
            for(String value:dependencie){
                String id = value.split(":")[0];
                String status = value.split(":")[1];
                Item el = projectitems.get(id);
                item.getDependencies().put(el, status);
            }
        }
        
        if(!test){
            if(RunnerRepository.getSuiteNr()>0){
                while(RunnerRepository.window.mainpanel.p1.sc.g==null){
                    try{Thread.sleep(10);}
                    catch(Exception e){e.printStackTrace();}}
                RunnerRepository.window.mainpanel.p1.sc.g.updateLocations(RunnerRepository.getSuita(0));
                RunnerRepository.window.mainpanel.p1.sc.g.repaint();}}
        else{if(RunnerRepository.getTestSuiteNr()>0){
                while(RunnerRepository.window==null||RunnerRepository.window.mainpanel==null||
                RunnerRepository.window.mainpanel.getP2()==null||RunnerRepository.window.mainpanel.getP2().sc==null||
                RunnerRepository.window.mainpanel.getP2().sc.g==null){
                    try{Thread.sleep(10);}
                    catch(Exception e){e.printStackTrace();}}
                RunnerRepository.window.mainpanel.getP2().sc.g.updateLocations(RunnerRepository.getTestSuita(0));
                RunnerRepository.window.mainpanel.getP2().sc.g.repaint();}}}}
