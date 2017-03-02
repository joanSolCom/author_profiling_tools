package LMAO.ROFL;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.apache.commons.io.Charsets;
import org.apache.commons.io.FileUtils;

import edu.arizona.sista.processors.Document;
import edu.arizona.sista.processors.fastnlp.FastNLPProcessor;


public class App 
{

    public static void main( String[] args ) throws IOException
    {
    	FastNLPProcessor proc = new FastNLPProcessor(true,false, true);
    	   	
    	File [] inputs = new File("INPUT RAW PATH").listFiles();
    	
    	for(File input:inputs){
			String outPath = "OUTPUT DISCOURSE PATH"+input.getName();
    		File outFile = new File(outPath);
    		if(!outFile.exists())
    		{
    			String content = FileUtils.readFileToString(input, StandardCharsets.UTF_8);
        		try
        		{
        			Document doc = proc.annotate(content, false);
                	String tree = doc.discourseTree().toString();
                	FileUtils.writeStringToFile(new File(outPath), tree, StandardCharsets.UTF_8,false);
                	System.out.println("PROCESSED " + input.getName());
        		}
        		catch(Exception e)
        		{
        			System.out.println("error with " + input.getName());
        			continue;
        		}
    		}
     	}
    }
    
    public static void main_PAN( String[] args ) throws IOException
    {
        FastNLPProcessor proc = new FastNLPProcessor(true,false, true);
        File [] inputs = new File("/home/joan/Escritorio/Datasets/PANEssays/Test/").listFiles();
        
        for(File input:inputs)
        {
            if(input.isDirectory())
            {   
                int i = 0;
                while(i<7)
                {  
                    File fdIn = new File(input.getAbsolutePath()+"/known0"+i+".txt");
                    File fdOut = new File(input.getAbsolutePath()+"/known0"+i+".txt_disc");

                    if(!fdOut.exists() && fdIn.exists())
                    {	System.out.println(input.getName());
                        String content = FileUtils.readFileToString(fdIn, StandardCharsets.UTF_8);
                        try
                        {
                            Document doc = proc.annotate(content, false);
                            String tree = doc.discourseTree().toString();
                            FileUtils.writeStringToFile(fdOut, tree, StandardCharsets.UTF_8,false);
                        	System.out.println("PROCESSED " + fdIn.getName());
                        }
                        catch(Exception e)
                        {
                            System.out.println("error with " + fdIn.getName());
                            continue;
                        }

                    }
                    i++;
                }
                File fdInUnk = new File(input.getAbsolutePath()+"/unknown.txt");
                File fdOutUnk = new File(input.getAbsolutePath()+"/unknown.txt_disc");

                if(!fdOutUnk.exists() && fdInUnk.exists())
                {
                    String contentUnk = FileUtils.readFileToString(fdInUnk, StandardCharsets.UTF_8);
                    try
                    {
                        Document docUnk = proc.annotate(contentUnk, false);
                        String treeUnk = docUnk.discourseTree().toString();
                        FileUtils.writeStringToFile(fdOutUnk, treeUnk, StandardCharsets.UTF_8,false);
                    	System.out.println("PROCESSED " + fdInUnk.getName());

                    }
                    catch(Exception e)
                    {
                        System.out.println("error with " + fdInUnk.getName());
                        continue;
                    }

                }

                
            }
            
        }

    }
}
