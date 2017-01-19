package root.nrc_workspace.src;

import java.util.*;

public class SubGraphsContenuti implements Comparable{

	private String comp;
	private ArrayList<String> fragms;
 
	public SubGraphsContenuti(String com){
		this.comp = com;     	//codice del composto
		this.fragms = new ArrayList<String>();
	}
	
	
	public void addSubGraph(String fragm){
		fragms.add(fragm); 		
	}
 
	public String getSequenceID(){
		return( comp );
	}
	
	public ArrayList getSubGraph(){
		return( fragms );
	}

	
	public int compareTo(Object obj ){
		
		if ( equals( obj ) )
			return 0;

	    SubGraphsContenuti altro = (SubGraphsContenuti)obj;
//	    if (Integer.valueOf(comp) < Integer.valueOf(altro.comp)) //buona per interi
	    if ( comp.compareTo(altro.comp) < 0 )					 //buona per stringhe
	    	return -1;

//	    if (Integer.valueOf(comp) > Integer.valueOf(altro.comp)) //buona per interi    
	    else if ( comp.compareTo(altro.comp) > 0 )				 //buona per stringhe
	    	return 1;
    
	    return 0;
	}
	
}
