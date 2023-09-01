import java.net.InetAddress;

class NetworkScanner {
    public static void scan(String cidr) throws Exception {
        String[] parts = cidr.split("/");
        String subnet = parts[0];
        int prefixLength = Integer.parseInt(parts[1]);
        int subnetMask = 0xffffffff << (32 - prefixLength);
        byte[] bytes = new byte[]{
                (byte) (subnetMask >>> 24),
                (byte) (subnetMask >> 16 & 0xff),
                (byte) (subnetMask >> 8 & 0xff),
                (byte) (subnetMask & 0xff)
        };
        InetAddress address = InetAddress.getByAddress(subnetToBytes(subnet));
        for (int i = 1; i <= 254; i++) {
            byte[] currentBytes = subnetToBytes(subnet + "." + i);
            if ((currentBytes[3] & 0xff) == 0 || (currentBytes[3] & 0xff) == 255) {
                continue;
            }
            InetAddress currentAddress = InetAddress.getByAddress(currentBytes);
            if (address.getHostAddress().equals(currentAddress.getHostAddress())) {
                continue;
            }
            if (currentAddress.isReachable(1000)) {
                System.out.println(currentAddress.getHostAddress() + " is reachable");
            } else {
                System.out.println(currentAddress.getHostAddress() + " is not reachable");
            }
        }
    }

    private static byte[] subnetToBytes(String subnet) {
        String[] parts = subnet.split("\\.");
        byte[] bytes = new byte[4];
        for (int i = 0; i < 4; i++) {
            bytes[i] = (byte) Integer.parseInt(parts[i]);
        }
        return bytes;
    }
}