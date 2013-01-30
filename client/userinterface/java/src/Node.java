import java.util.ArrayList;
import java.util.HashMap;

public class Node{
    private String id,path,name;
    private HashMap<String,Node> children = new HashMap<String,Node>();
    private HashMap<String,String> properties = new HashMap<String,String>();

    public Node(String id, String path, String name){
        this.id = id;
        this.path = path;
        this.name=name;
    }
    
    public HashMap getChildren(){
        return children;
    }
    
    public HashMap getProperties(){
        return properties;
    }
    
    public String getID(){
        return id;
    }
    
    public String getPath(){
        return path;
    }
    
    public String getName(){
        return name;
    }
    
    public void gstID(String id){
        this.id=id;
    }
    
    public void setPath(String path){
        this.path=path;
    }
    
    public void setName(String name){
        this.name=name;
    }   
    
    public Node getChild(String id){
        return children.get(id);
    }
    
    public void addChild(String id, Node child){
        children.put(id, child);
    }
    
    public void removeChild(String id){
        children.remove(id);
    }
    
    public String getPropery(String name){
        return properties.get(name);
    }
    
    public void addProperty(String name, String value){
        properties.put(name, value);
    }
    
    public void setPropery(String name, String value){
        properties.put(name, value);
    }
    
    public void removeProperty(String name){
        properties.remove(name);
    }
    
    public String toString(){
        return this.name;
    }
}