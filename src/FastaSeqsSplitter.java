package root.nrc_workspace.src;

/**
 * This tool aims to chop the file in various parts based on the number of sequences required in one file.
 */

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;


/**
 * @author fiannaca@pa.icar.cnr.it
 * 
 */
public class FastaSeqsSplitter implements Serializable{




	public void chopFile(String fileName, String filePath) throws IOException, ClassNotFoundException {
		Map<String, String> mapID2Type = new HashMap<String, String>();
		byte[] allBytes = null;
		String outFileName = fileName.substring(0, fileName.length() -3); //file ".fa"
		//System.out.println(outFileName);
		try {

			allBytes = Files.readAllBytes(Paths.get(fileName));
		} catch (IOException e) {
			e.printStackTrace();
		}

		String allLines = new String(allBytes, StandardCharsets.UTF_8);
		//   System.out.println(allLines);

		// Using a clever cheat with help from stackoverflow
		String cheatString = allLines.replace(">", "~>");
		//cheatString = cheatString.replace("\\s+", "");
		String[] splitLines = cheatString.split("~");
		System.out.println("aa"+splitLines[1]);

		for (int i=1 ; i < splitLines.length; i++){
			FileWriter fw = null;
			String sequenceName= splitLines[i].split(" ")[0].substring(1);
			String sequenceID= splitLines[i].split(" ")[0].concat(".fa").substring(1); //elimino il > ad inizio riga
			if (sequenceID.contains("|"))
				sequenceID= sequenceID.split("|")[2]; //per i piRNA
			//	        	System.out.println(outputFile);

			String type= splitLines[i].split(" ")[4].split(":")[1];
			mapID2Type.put(sequenceName, type);



			fw = new FileWriter(new String(filePath + "/" + sequenceID));
			//System.out.println(filePath+"/"+sequenceID);
			fw.write(splitLines[i]);
			fw.close();
		}


		/*Serializzazione*/
		FileOutputStream fileOut =new FileOutputStream(filePath+"/hashIdType");
		ObjectOutputStream out = new ObjectOutputStream(fileOut);

		out.writeObject(mapID2Type);
		out.close();

		
		FileInputStream fileIn = new FileInputStream(filePath+"/hashIdType");
        ObjectInputStream in = new ObjectInputStream(fileIn);
        Map<String, String> e = (HashMap) in.readObject();
        
        Set<String> key = e.keySet();
        Iterator<String> it = key.iterator();
        
        ;
		while(it.hasNext()){
        	String s = it.next();
        	System.out.println(s+","+e.get(s));
		}

	}



	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		String dataset_name=args[0];
		String path=args[1];
		FastaSeqsSplitter fc = new FastaSeqsSplitter();
		try {
			System.out.println(System.getProperty("user.dir"));
			fc.chopFile(dataset_name,path);
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
