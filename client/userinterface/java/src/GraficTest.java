/*
File: GraficTest.java ; This file is part of Twister.
Version: 2.001

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
import java.awt.Canvas;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.Rectangle;
import java.awt.Font;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.PrintStream;
import javax.imageio.ImageIO;
import javax.swing.JPanel;
import java.awt.Dimension;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.awt.event.KeyListener;
import java.awt.event.KeyEvent;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;

public class GraficTest extends JPanel{
    private static final long serialVersionUID = 1L;
    private boolean applet;
    private ArrayList <Integer> selected;
    private boolean foundfirstitem;
    private int y = 5;
    private byte keypress=0;
    private ArrayList <Item> selecteditems = new ArrayList<Item>();
    private int maxWidth = 0;

    public GraficTest(int x, int y, boolean applet){
        this.applet = applet;
        setFocusable(true);
        
        setSize(445, 595);
        setBackground(new Color(190, 195, 195));
        addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                handleClick(ev);}
            public void mouseEntered(MouseEvent ev){
                requestFocus();
            }
        });
        addKeyListener(new KeyListener(){
            public void keyPressed(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_SHIFT){keypress=1;}
                if(ev.getKeyCode()==KeyEvent.VK_CONTROL){keypress=2;}}                
            public void keyTyped(KeyEvent ev){}            
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_SHIFT ||
                ev.getKeyCode()==KeyEvent.VK_CONTROL){
                    keypress=0;}}});
    }
    
    public boolean isParentSelected(ArrayList<Item>items,Item item){
        ArrayList<Integer>pos = (ArrayList<Integer>)item.getPos().clone();
        pos.remove(pos.size()-1);
        Item parent = getCloneItem(items,pos);
        if(parent!=null){
            if(parent.isSelected()){
                return true;
            }
            return isParentSelected(items,parent);}
        return false;
    }
    
    /*
     * prints this item and his 
     * subitems indices on screen
     */
    public void printPos(Item item){
        if(item.getType()==0||item.getType()==1||item.getType()==2){
            System.out.print(item.getName()+" - ");
            for(int i=0;i<item.getPos().size();i++){
                System.out.print(item.getPos().get(i));}
            System.out.println();}
        if(item.getType()==1){
            for(int i=0;i<item.getSubItemsNr();i++){
                printPos(item.getSubItem(i));}}
        if(item.getType()==2){
            for(int i=0;i<item.getSubItemsNr();i++){
                printPos(item.getSubItem(i));}}}
    
    /*
     * deselect all the items that are selected
     */
    public void deselectAll(){
        for(Item item:selecteditems){
            item.select(false);
        }
        selecteditems.clear();
    }
    
    /*
     * interpret mouse click
     */
    public void handleClick(MouseEvent ev){
        if(ev.getButton()==1){
            if(Repository.getTestSuiteNr()==0)return;            
            if(keypress==0){
                deselectAll();
                getClickedItem(ev.getX(),ev.getY());
                selectItem(selected);
                Item item = getItem(selected);
                if(item==null||item.getType()!=1)return;
                Item parent = Repository.window.mainpanel.p1.sc.g.getParent(item,true);
                String[] eps = parent.getEpId();
                ArrayList<Log> logs = new ArrayList<Log>();
                for(Log l:Repository.window.mainpanel.getP2().logs){
                    for(String s:eps){
                        if((s.split(" : ")[0]+"_"+Repository.getLogs().get(4)).equals(l.log)){
                            logs.add(l);
                        }
                    }                    
                }
                for(Log l:logs){
                    l.findNext(item.getName()+"` >>>",true,"<<< START filename: `");
                }
            }
            else if(keypress==2){
                getClickedItem(ev.getX(),ev.getY());
                Item item = getItem(selected);
                if(item.getType()!=0){
                    if(item!=null && item.isSelected()){
                        item.select(false);
                        selecteditems.remove(item);
                    }
                    else{
                        item.select(true);
                        selecteditems.add(item);
                    }
                }
            }
            else{
                deselectAll();
                int [] theone1 = new int[selected.size()];
                for(int i=0;i<selected.size();i++){theone1[i]= selected.get(i).intValue();}
                getClickedItem(ev.getX(),ev.getY());
                int [] theone2 = new int[selected.size()];
                for(int i=0;i<selected.size();i++){theone2[i]= selected.get(i).intValue();}
                if(theone1.length==theone2.length){
                    if(theone1.length>1){
                        int [] temp1,temp2;
                        temp1 = Arrays.copyOfRange(theone1,0,theone1.length-1);
                        temp2 = Arrays.copyOfRange(theone2,0,theone2.length-1);
                        if(Arrays.equals(temp1,temp2)){
                            int [] first,second;
                            if(theone2[theone2.length-1]>=theone1[theone1.length-1]){
                                first = theone2;
                                second = theone1;}
                            else{
                                first = theone1;
                                second = theone2;}
                            ArrayList<Integer>temp11 = new ArrayList<Integer>();
                            for(int i=0;i<temp1.length;i++)temp11.add(new Integer(temp1[i]));
                            Item parent = getItem(temp11);
                            for(int i=second[second.length-1];i<first[first.length-1]+1;i++){
                                ArrayList<Integer> temporary = new ArrayList<Integer>();
                                for(int m=0;m<parent.getSubItem(i).getPos().size();m++){
                                    temporary.add(new Integer(parent.getSubItem(i).getPos().get(m).intValue()));}
                                selectItem(temporary);}}}
                    else{
                        int first,second;
                        if(theone1[0]>=theone2[0]){
                            first = theone1[0];
                            second = theone2[0];}
                        else{
                            second = theone1[0];
                            first = theone2[0];}
                        for(int m=second;m<first+1;m++){
                            selectItem(Repository.getTestSuita(m).getPos());}}}}
            if(selected.size()>0&&getItem(selected).getType()==2&&ev.getClickCount()==2){
                if(getItem(selected).getSubItemsNr()>0){
                    getItem(selected).setVisible(!(getItem(selected).getSubItem(0).isVisible()));}
                updateLocations(getItem(selected));}
            repaint();}
        if(ev.getButton()==3&&selecteditems.size()>0){
            popUp(ev);}}
           
    /*
     * method to display popup
     */
    public void popUp(MouseEvent ev){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Run separately");        
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev2){
                runSeparately();
            }});
        p.show(this,ev.getX(),ev.getY());
    }
    

    public void runSeparately(){
        String userrespons = CustomDialog.showInputDialog(JOptionPane.INFORMATION_MESSAGE, 
                                                            JOptionPane.OK_CANCEL_OPTION, 
                                                            GraficTest.this, "", "Number of times:");
        final int times;
        try{times = Integer.parseInt(userrespons);}//exit if respons is not integer
        catch(Exception e){
            return;
        }
        ArrayList<Item> items = cloneItems();//clone all testcases
        ArrayList<Item> fordelete = new ArrayList<Item>();//array to hold the ones to delete
        
        for(Item item:items){
            if(!item.isSelected()&&
            !hasSubItemSelected(item)
            &&!isParentSelected(items, item)){
                fordelete.add(item);
            }
            else{
                for(Item child:item.getSubItems()){
                    removeSelected(items,fordelete,item,child);
                }
            }
        }  
        ArrayList<Item> parents = new ArrayList<Item>();//parents array for items in fordelete
        ArrayList<Integer>pos;                          //array
        for(Item item:fordelete){
            pos = (ArrayList<Integer>)item.getPos().clone();
            pos.remove(pos.size()-1);
            parents.add(getCloneItem(items,pos));
        }
        for(int i=0;i<fordelete.size();i++){
            if(parents.get(i)!=null){
                parents.get(i).getSubItems().remove(fordelete.get(i));
            }
            else{
                items.remove(fordelete.get(i));
            }
        }
        for(Item it:items){//separate TB from ep 
            it.setEpId(new String[]{it.getEpId()[0].split(" : ")[1]});
        }
        ArrayList<Item>last = new ArrayList<Item>();//array to store items repeatedly
        for(int i=0;i<times;i++){                   //the number of times the user specified
            for(Item it:items){
                last.add(it);
            }
        }
        if(!writeXML(last)){
            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                  GraficTest.this, "Failed", 
                                  "File could not be saved");
//             CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE, 
//                                   GraficTest.this, "Succes", 
//                                   "File succesfuly saved");
        }
//         else {
//             CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
//                                   GraficTest.this, "Failed", 
//                                   "File could not be saved");
//         }
    }
    
    public void printName(Item item){
        System.out.println(item.getName());
        for(Item i:item.getSubItems()){
            printName(i);
        }
    }
    
    /*
     * convret ArrayList last to xml
     * and upload it as a file 
     */
    public boolean writeXML(ArrayList<Item>last){
        try{XMLBuilder xml = new XMLBuilder(last);
            xml.createXML(true,false,true,
                          Repository.window.mainpanel.p1.suitaDetails.getPreScript(),
                          Repository.window.mainpanel.p1.suitaDetails.getPostScript(),
                          Repository.window.mainpanel.p1.suitaDetails.saveDB(),
                          Repository.window.mainpanel.p1.suitaDetails.getDelay(),
                          Repository.window.mainpanel.p1.suitaDetails.getGlobalLibs());
            String dir = Repository.getXMLRemoteDir();
            String [] path = dir.split("/");
            StringBuffer result2 = new StringBuffer();
            if (path.length > 0){
                for (int i=0; i<path.length-1; i++){
                    result2.append(path[i]);
                    result2.append("/");}}
            final String filelocation = result2.toString()+"testsuites_temp.xml";
            if(!xml.writeXMLFile("testsuites_temp.xml", false,true)) return false;
            new Thread(){
                public void run(){
                    try{
                        String result = Repository.getRPCClient().execute("runTemporary",
                                                            new Object[]{Repository.getUser(),
                                                                            filelocation})+"";
                        if(result.indexOf("ERROR")!=-1){
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                                  GraficTest.this, "Failed", 
                                                  result);
                        }
                    }
                    catch(Exception e){
                        e.printStackTrace();
                    }
                }
            }.start();
            return true;
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    /*
     * check if any of its
     * subitems is selected
     */
    public boolean hasSubItemSelected(Item item){
        for(Item subitem:item.getSubItems()){
            if(subitem.isSelected())return true;
        }
        for(Item subitem:item.getSubItems()){
            if(hasSubItemSelected(subitem))return true;
        }
        return false;
    }
    
    /*
     * adds item to remove
     * from his parent if item 
     * is not selected or is not in a 
     * selected tree
     */
    public void removeSelected(ArrayList<Item>items, ArrayList<Item>fordelete, Item parent, Item child){
        if(!child.isSelected()&&!hasSubItemSelected(child)&&child.getType()!=0
        &&!isParentSelected(items,child)){
            fordelete.add(child);
            return;
        }
        if(child.getSubItemsNr()>0){
            for(Item subchild:child.getSubItems()){
                removeSelected(items,fordelete,child,subchild);
            }
        }
    }
    
    /*
     * creates a clone of all
     * tc's from test suite
     */
    public ArrayList<Item> cloneItems(){
        ArrayList<Item> items = new ArrayList<Item>();
        for(Item i:Repository.getTestSuite()){
            items.add(i.clone());
        }
        return items;
    }
            
    /*
     * select item based on
     * his pos indices
     */
    public void selectItem(ArrayList <Integer> pos){
        Item item = getItem(pos);
        if(item!=null&&item.getType()!=0){
            item.select(true);        
            selecteditems.add(item);}}
            
    /*
     * get item based on ArrayList indices
     */
    public Item getCloneItem(ArrayList<Item>clone,ArrayList <Integer> pos){
        if(pos.size()>0){
            Item theone1 = clone.get(pos.get(0));
            for(int j=1;j<pos.size();j++){
                theone1 = theone1.getSubItem(pos.get(j));}
            return theone1;}
        return null;}
    
    /*
     * get item based on ArrayList indices
     */
    public Item getItem(ArrayList <Integer> pos){
        if(pos.size()>0){
            Item theone1 = Repository.getTestSuita(pos.get(0));
            for(int j=1;j<pos.size();j++){
                theone1 = theone1.getSubItem(pos.get(j));}
                return theone1;}
        return null;}
    
    /*
     * return item on location x,y
     */
    public void getClickedItem(int x, int y){
        Rectangle r = new Rectangle(x-1,y-1,2,2);
        int suitenr = Repository.getTestSuiteNr();
        selected = new ArrayList<Integer>();
        for(int i=0;i<suitenr;i++){
            if(handleClicked(r,Repository.getTestSuita(i))){
                selected.add(i);
                break;}}
        if(selected.size()>0)Collections.reverse(selected);}
     
    /*
     * handle click on specific item
     */
    public boolean handleClicked(Rectangle r, Item item){
        if(r.intersects(item.getRectangle())&&item.isVisible())return true;
        else{int itemnr = item.getSubItemsNr();
            for(int i=0;i<itemnr;i++){
                if(handleClicked(r,item.getSubItem(i))){
                    selected.add(i);
                    return true;}}
            return false;}}
     
    /*
     * update items location in tree view
     * starting from suita
     */
    public void updateLocations(Item suita){
        ArrayList <Integer> selected2 = (ArrayList <Integer>)suita.getPos().clone();
        if(selected2.size()>1){
            int index = selected2.get(0);
            selected2.remove(0);
            for(int i=index;i<Repository.getTestSuiteNr();i++){   
                Repository.window.mainpanel.getP2().sc.g.iterateThrough(Repository.getTestSuita(i),selected2);
                selected2 = null;}}
        else if(selected2.size()==1){
            for(int i=selected2.get(0);i<Repository.getTestSuiteNr();i++){
                Repository.window.mainpanel.getP2().sc.g.iterateThrough(Repository.getTestSuita(i),null);}}
        y=10;
        foundfirstitem=false;
        updateScroll();}
        
    /*
     * calculates previous position
     * for aligning on x
     */
    public int calcPreviousPositions(Item item){
        /*
         * calc diferently based on item type
         */
        ArrayList <Integer> pos = (ArrayList <Integer>)item.getPos().clone();
        if(item.getType()!=0){//it is not a prop
            if(pos.size()>1){
                pos.remove(pos.size()-1);
                Item temp = getItem(pos);
                return temp.getLocation()[0]+(int)(temp.getRectangle().getWidth()/2+20);}
            else{return 5;}}
        else{// it is prop should put beside it
            pos.remove(pos.size()-1);
            Item temp = getItem(pos);
            return temp.getLocation()[0]+(int)(temp.getRectangle().getWidth()+20);}}
        
    /*
     * positions the item based on
     * previous location
     */    
    public void positionItem(Item item){    
        int x = 0;
        if(item.getType()!=0){
            x = calcPreviousPositions(item);
            item.setLocation(new int[]{x,y});
            y+=(int)(5+item.getRectangle().getHeight());}
        else{
            x = calcPreviousPositions(item);
            item.setLocation(new int[]{x,(int)(y-5-item.getRectangle().getHeight())});}
        if(item.getType()==0&&x>maxWidth){
            maxWidth = x;    
        }
    }
    
    /*
     * iterate through subitem of an item
     * and position it
     */
    public void iterateThrough(Item item, ArrayList <Integer> theone){
        int subitemsnr = item.getSubItemsNr();
        if(theone==null){
            if(item.isVisible()){
                if(!foundfirstitem)y=item.getLocation()[1];
                foundfirstitem = true;
                positionItem(item);}
            for(int i=0;i<subitemsnr;i++){    
                iterateThrough(item.getSubItem(i),null);}}
        else if(theone.size()>1){
            int index = theone.get(0);
            theone.remove(0);
            for(int i=index;i<subitemsnr;i++){
                iterateThrough(item.getSubItem(i),theone);
                theone=null;}}
        else if(theone.size()==1){
            int index = theone.get(0);
            for(int i=index;i<subitemsnr;i++){
                iterateThrough(item.getSubItem(i),null);}}}
                
    /*
     * update scroll to adjust based
     * on view dimension
     */
    public void updateScroll(){
//         System.out.println("Update Scroll: "+(maxWidth+100));
        int y1=0;
        for(int i=0;i<Repository.getTestSuiteNr();i++){
            if(Repository.getTestSuita(i).isVisible()){
                y1 = getLastY(Repository.getTestSuita(i),y1);
            }
        }
        setPreferredSize(new Dimension(maxWidth+120,y1+10));
        if(y1>getHeight()){
            setPreferredSize(new Dimension(maxWidth+120,y1+10));
//             setPreferredSize(new Dimension(425,y1+10));
            Repository.window.mainpanel.getP2().sc.revalidate();}
        if(getHeight()>595){
            if(y1<getHeight()-10){
//                 setPreferredSize(new Dimension(425,y1+10));
                setPreferredSize(new Dimension(maxWidth+120,y1+10));
                Repository.window.mainpanel.getP2().sc.revalidate();}
            if(y1<595){
//                 setPreferredSize(new Dimension(445,595));
                setPreferredSize(new Dimension(maxWidth+120,595));
                Repository.window.mainpanel.getP2().sc.revalidate();}}}
          
                
    /*
     * return last y position for last visible item
     */
    public int getLastY(Item item, int height){
        if(height<=(item.getRectangle().getY()+item.getRectangle().getHeight())){
            height=(int)(item.getRectangle().getY()+item.getRectangle().getHeight());        
            int nr = item.getSubItemsNr()-1;
            for(int i=nr;i>=0;i--){
                if(item.getSubItem(i).isVisible()){height = getLastY(item.getSubItem(i),height);}}
            return height;}
        else return height;}

    public void paint(Graphics g){
        g.setColor(Color.WHITE);
        g.fillRect(0,0,getWidth(),getHeight());
        g.setColor(Color.BLACK);
        int suitenr = Repository.getTestSuiteNr();
        for(int i=0;i<suitenr;i++){
            handlePaintItem(Repository.getTestSuita(i),g);}}
            
    public void handlePaintItem(Item item, Graphics g){
        drawItem(item,g);
        if(item.getSubItemsNr()>0&&item.getSubItem(0).isVisible()){
            for(int i=0;i<item.getSubItemsNr();i++){
                if(!item.getSubItem(i).isVisible())continue;
                handlePaintItem(item.getSubItem(i),g);}
        }
    }
             
            
    /*
     * handle drawing item based on
     * item type and it's properties
     */
    public void drawItem(Item item,Graphics g){
         if(item.isSelected()){
            g.setColor(new Color(220,220,220));
            g.fillRect((int)item.getRectangle().getX(),(int)item.getRectangle().getY(),
                        (int)item.getRectangle().getWidth(),(int)item.getRectangle().getHeight());
            g.setColor(Color.BLACK);
            g.drawRect((int)item.getRectangle().getX(),(int)item.getRectangle().getY(),
                        (int)item.getRectangle().getWidth(),(int)item.getRectangle().getHeight());}
        g.setColor(Color.BLACK);
        g.setFont(new Font("TimesRoman", Font.PLAIN, 12));
        if(item.getType()==2){
            g.drawString(item.getName(),(int)item.getRectangle().getX()+25,
                        (int)item.getRectangle().getY()+18);
            g.drawImage(Repository.getSuitaIcon(),(int)item.getRectangle().getX()+5,
                       (int)item.getRectangle().getY()+1,null);}
        else if(item.getType()==1){
            if(!item.isRunnable())g.setColor(Color.GRAY);
            String name = item.getName();
            try{name = item.getName().split(Repository.getTestSuitePath())[1];}
            catch (Exception e){name = item.getName();};
            g.drawString(name,(int)item.getRectangle().getX()+30,(int)item.getRectangle().getY()+15);
            g.setColor(Color.BLACK);
            String value = item.getSubItem(0).getValue().toUpperCase();
            if(value.equals("FAIL")) g.drawImage(Repository.getFailIcon(),
                                                (int)item.getRectangle().getX()+5,
                                                (int)item.getRectangle().getY()+1,null);
            else if(value.equals("PENDING")) g.drawImage(Repository.getPendingIcon(),
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("RUNNING")) g.drawImage(Repository.getWorkingIcon(),
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("SKIPPED")) g.drawImage(Repository.getSkippedIcon(), 
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("STOPPED")) g.drawImage(Repository.getStoppedIcon(), 
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("NOT EXECUTED")) g.drawImage(Repository.getNotExecIcon(), 
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("TIMEOUT")) g.drawImage(Repository.getTimeoutIcon(),
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("WAITING")) g.drawImage(Repository.getWaitingIcon(),
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("PASS")) g.drawImage(Repository.getPassIcon(),
                   (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else g.drawImage(Repository.getTCIcon(),(int)item.getRectangle().getX()+5,
                            (int)item.getRectangle().getY()+1,null);}
        else{
//             g.drawImage(Repository.getPropertyIcon(),(int)item.getRectangle().getX()+2,(int)item.getRectangle().getY()+1,null);
//             g.drawString(item.getName()+" : "+item.getValue(),(int)item.getRectangle().getX()+25,(int)item.getRectangle().getY()+15);
//             System.out.println(item.getName()+" : "+item.getValue()+" "+maxWidth+2+" "+(int)item.getRectangle().getY()+1);
            g.drawImage(Repository.getPropertyIcon(),maxWidth+2,(int)item.getRectangle().getY()+1,null);
            g.drawString(item.getName()+" : "+item.getValue(),maxWidth+25,(int)item.getRectangle().getY()+15);
        }
        if((item.getPos().size()!=1)){
            if(item.getType()==0){}
            else{
                g.drawLine((int)item.getRectangle().getX()-25,
                           (int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),
                           (int)item.getRectangle().getX(),
                           (int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2));
                ArrayList<Integer> temp = (ArrayList<Integer>)item.getPos().clone();
                if(temp.get(temp.size()-1)==0)g.drawLine((int)item.getRectangle().getX()-25,
                                                         (int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),
                                                         (int)item.getRectangle().getX()-25,
                                                         (int)(item.getRectangle().getY())-5);
                else{
                    temp.set(temp.size()-1,new Integer(temp.get(temp.size()-1).intValue()-1));
                    Item theone = getItem(temp);
                    g.drawLine((int)item.getRectangle().getX()-25,
                               (int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),
                               (int)item.getRectangle().getX()-25,
                               (int)(theone.getRectangle().getY()+theone.getRectangle().getHeight()/2));}}}
        if(item.getEpId()!=null&&item.getEpId().length>0){
            StringBuilder EP = new StringBuilder();
            for(String s:item.getEpId()){
                EP.append(s+";");
            }
            EP.deleteCharAt(EP.length()-1);
            g.setFont(new Font("TimesRoman", Font.PLAIN, 11));
            g.drawString(" - "+EP.toString(),(int)(item.getRectangle().getX()+item.getRectangle().getWidth()-100),
                                              (int)(item.getRectangle().getY()+18));}}}
