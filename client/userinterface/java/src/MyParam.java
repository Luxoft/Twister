import org.w3c.dom.Node;
class MyParam{
    private Node name,value;
    
    public void setValue(Node value){
        this.value=value;
    }
    
    public void setName(Node name){
        this.name=name;
    }
    
    public Node getValue(){
        return value;
    }
    
    public Node getName(){
        return name;
    }
    
    public String toString(){
        return name.getNodeValue()+" : "+value.getNodeValue();
    }
}