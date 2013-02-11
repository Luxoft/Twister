import org.w3c.dom.Node;

class MyFolder{
    private Node node;
    
    public MyFolder(Node node){
        this.node = node;
    }
    
    public Node getNode(){
        return node;
    }
    
    public String toString(){
        return node.getNodeValue();
    }
}