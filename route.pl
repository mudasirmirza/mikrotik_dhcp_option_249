#!/usr/bin/perl -w

use strict;

    print "\033[2J";    #clear the screen
    print "\033[0;0H";  #jump to 0,0

sub option_121 {
    my $gw = shift;
    my $string = '';
    my ($subnet, $mask, $b0, $b1, $b2, $b3);
    foreach my $cidr (@_) {
        ($subnet,  $mask) = split('/', $cidr);
        ($b0, $b1, $b2, $b3) = split(/\./, $subnet);
        $string .= sprintf('%02x', $mask);
        $string .= sprintf('%02x', $b0) if($mask > 0);
        $string .= sprintf('%02x', $b1) if($mask > 8);
        $string .= sprintf('%02x', $b2) if($mask > 16);
        $string .= sprintf('%02x', $b3) if($mask > 24);
        $string .= sprintf('%02x%02x%02x%02x', split(/\./, $gw));
    }
    return $string;
}

if(@ARGV < 2)
{
    print "\n";
    print "Usage: $0 [gateway] [host|network]/[bitmask]\n\n";
    print "Example: $0 192.168.0.1 192.168.10.0/24\n\n";
}
elsif($ARGV[0] =~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/)
{
    print "DHCP option 121 (249) hex string: ".option_121(@ARGV)."\n";
}
else
{
    print "Invalid gateway IP address: '$ARGV[0]'\n";
}
