/*
File: Item.java ; This file is part of Twister.
Version: 2.007
Copyright (C) 2012 , Luxoft

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
package com.twister;

import java.awt.Rectangle;
import java.util.ArrayList;

public class Item implements Cloneable{
    private int type;//2-suite,1-tc,0-prop 
    private String name,value;//name, value if prop
    private boolean selected = false;//used for graphic representation
    private Rectangle rectangle=new Rectangle();// rectangle occupied by this item in graphics
    private Rectangle checkrectangle=new Rectangle(); // check rectangle occupied by this item in graphics
    private boolean visible = true;
    private ArrayList <Item> subitems = new ArrayList<Item>();
    private ArrayList <Integer> indexpos;//the index of this item in suite tree
    private boolean check = true;
    private String [] EpID = {};
    private boolean runnable = true;
    private ArrayList<String[]> userDefined = new ArrayList<String[]>();//name value pair
    private boolean prerequisite = false;
    private boolean teardown = false;
    private boolean optional = false;
    private String [] servers,libs;
    private String [] configurations = {}; 
    private boolean panicdetect = false;
    private int ceindex;
    private boolean clearcase = false;
    
    
    public int getCEindex() {
		return ceindex;
	}

	public void setCEindex(int ceindex) {
		this.ceindex = ceindex;
	}

	public String[] getLibs() {
		return libs;
	}

	public void setLibs(String[] libs) {
		this.libs = libs;
	}

	public Item(String name,int type, int x, int y, int width, int height, ArrayList <Integer> indexpos){
        this.indexpos = indexpos;
        this.type = type;
        this.name = name;
        rectangle.setLocation(x,y);
        rectangle.setSize(width,height);
        if(type!=0){
            checkrectangle.setLocation(x+3,y+3);
            checkrectangle.setSize(height-6,height-6);}}
            
    public void setPrerequisite(boolean prerequisite){
        this.prerequisite = prerequisite;
        if(prerequisite){
            setCheck(true,true);
            setRunnable(true);}}
    
    public void setTeardown(boolean teardown){
        this.teardown = teardown;
        if(teardown){
            setCheck(true,true);
            setRunnable(true);}}
    
    public boolean isTeardown(){
        return teardown;}
        
    public boolean isPrerequisite(){
        return prerequisite;}
    
    public void setName(String name){
        this.name = name;}
        
    public String getName(){
        return name;}
        
    @SuppressWarnings("unchecked")
	public Item clone(){
        try{Item clone = (Item)super.clone();
            clone.subitems = (ArrayList <Item>)subitems.clone();
            for(int i=0;i<clone.getSubItemsNr();i++){clone.subitems.set(i, clone.getSubItem(i).clone());}
            return clone;}
        catch(CloneNotSupportedException e){
            e.printStackTrace();
            return null;}}
        
    public void setSubItemVisible(boolean visible){
        this.visible = visible;
        if(getType()==2){
        	int subitemsnr = subitems.size();
        	for(int i=0;i<subitemsnr;i++) getSubItem(i).setSubItemVisible(visible);
        }	
    }
        
    public void setVisible(boolean visible){
    	if(getType()==2){
    		int subitemsnr = subitems.size();
    		for(int i=0;i<subitemsnr;i++) getSubItem(i).setSubItemVisible(visible);
    	}
    }
        
    public void setVisibleTC(){
        if(subitems.size()>0&&getSubItem(0).getType()==0){
            setVisible(false);}
        else{
            setVisible(true);
            int subitemsnr = subitems.size();
            for(int i=0;i<subitemsnr;i++) getSubItem(i).setVisibleTC();}}
        
    public boolean isVisible(){
        return visible;}
        
    public int getSubItemsNr(){
        return subitems.size();}
       
    public Item getSubItem(int nr){
        return subitems.get(nr);}
        
    public void updatePos(int index,Integer newvalue){
        indexpos.set(index,newvalue);
        for(int i=0;i<subitems.size();i++){
            subitems.get(i).updatePos(index,newvalue);}}
        
    public ArrayList<Item> getSubItems(){
        return subitems;}
     
    public void addSubItem(Item s){
        subitems.add(s);}
     
    public void insertSubItem(Item s, int index){
        subitems.add(index,s);}
        
    public void select(boolean select){
        selected = select;}
        
    public void selectAll(Item item,boolean select){
        item.select(select);
        for(int i=0;i<item.getSubItemsNr();i++){selectAll(item.getSubItem(i),select);}}
        
    public boolean isSelected(){
        return selected;}
        
    public Rectangle getCheckRectangle(){
        return checkrectangle;}
        
    public Rectangle getRectangle(){
        return rectangle;}
    
    public void setRectangle(Rectangle rectangle){
        this.rectangle = rectangle;}
        
    public void setLocation(int [] pos){
        getRectangle().setLocation(pos[0],pos[1]);
        if(type!=0) checkrectangle.setLocation(pos[0]+3,pos[1]+3);}
        
    public int[] getLocation(){
        return (new int [] {(int)rectangle.getLocation().getX(),(int)rectangle.getLocation().getY()});}
        
    public String[] getEpId(){
        return EpID;}
        
    public void setEpId(String[] EpID){
        this.EpID = EpID;
        for(Item item:subitems){
            if(item.getType()==2)item.setEpId(EpID);}}
    
    public void setCheck(boolean check, boolean propagate){
        this.check = check;
        if(type==2&&propagate){
            int nr = subitems.size();
            for(int i=0;i<nr;i++){
                subitems.get(i).setCheck(check,propagate);}}
        else{
            if(getSubItemsNr()>0) subitems.get(0).setValue(check+"");}}
        
    public boolean getCheck(){
        return check;}
    
    public void setRunnable(boolean cond){
        runnable = cond;}  
        
    public void switchRunnable(){
        runnable = !runnable;}
        
    public boolean isRunnable(){
        return runnable;}
    
    public boolean isClearcase() {
		return clearcase;
	}

	public void setClearcase(boolean clearcase) {
		this.clearcase = clearcase;
	}

	public int getType(){
        return type;}
        
    public String getValue(){
        return value;}
        
    public String getFileLocation(){
        return name;}
        
    public void setValue(String value){
        this.value = value;}
        
    public void setPos(ArrayList<Integer> indexpos){
        this.indexpos=indexpos;
        for(int i=0;i<getSubItemsNr();i++){
			ArrayList<Integer> clona = (ArrayList<Integer>)indexpos.clone();
            clona.add(new Integer(i));
            getSubItem(i).setPos(clona);}}
            
    public boolean contains(Item item,Item test){
        if(test==null){
            if(this==item)return true;}
        else{
            if(test==item)return true;
            else{
                for(int i=0;i<getSubItemsNr();i++){
                    if(contains(item,getSubItem(i))){
                        return true;}}}}
        return false;}
        
    public void addUserDef(String [] userdef){
        userDefined.add(userdef);}
        
    public int getUserDefNr(){
        return userDefined.size();}
        
    public ArrayList<String[]>getUserDefs(){
        return userDefined;}
        
    public String [] getUserDef(int i){
        return userDefined.get(i);}
        
    public void setUserDef(int index,String description,String userDef){
        if(userDefined.size()-1<index){
            for(int i=userDefined.size();i<index+1;i++){
                userDefined.add(new String[]{"",""});}}
        String temp [] = userDefined.get(index);
        temp[0] = description;
        temp[1] = userDef;
        userDefined.set(index, temp);}
    
    public String[] getConfigurations() {
		return configurations;
	}

	public void setConfigurations(String[] configurations) {
		this.configurations = configurations;
	}

	public ArrayList<Integer> getPos(){
        return indexpos;}

	public boolean isOptional() {
		return optional;
	}

	public void setOptional(boolean optional) {
		this.optional = optional;
	}

	public String[] getServers() {
		return servers;
	}

	public void setServers(String[] servers) {
		this.servers = servers;
	}

	public boolean isPanicdetect() {
		return panicdetect;
	}

	public void setPanicdetect(boolean panicdetect) {
		this.panicdetect = panicdetect;
	}
}