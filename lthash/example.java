
package lthash;

/**
 * main
 */
public class example {

    public static void main(String[] args){
        
        System.out.println("Hello from the dark side");
        LtHash32 ltHash = new LtHash32();

        // Create an initial checksum of the values in input
        ltHash.add("apple".getBytes(), "orange".getBytes());
        byte[] checksum = ltHash.getChecksum();

        // Remove the hash of "apple" from the checksum and check
        // if the 2 checksums are equals
        ltHash.remove("apple".getBytes());
        boolean isEqual = ltHash.checksumEquals(checksum);

        // Update the hash of "orange" with the new value "apple"
        // and check if the 2 checksums are equals
        ltHash.update("orange".getBytes(), "apple".getBytes());
        isEqual = ltHash.checksumEquals(checksum);

        // Adding again the missing "orange" and check if the
        // checksum has gotten back to the initial status
        ltHash.add("orange".getBytes());
        isEqual = ltHash.checksumEquals(checksum);
        System.out.println(isEqual);
        System.out.println(checksum);
        
    }
    
}
