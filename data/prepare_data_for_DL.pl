#!/usr/bin/perl

use Geohash;
use Geohash qw(ADJ_RIGHT);
use Geohash qw(ADJ_LEFT);
use Geohash qw(ADJ_TOP);
use Geohash qw(ADJ_BOTTOM);

# https://metacpan.org/pod/Data::CosineSimilarity
use Data::CosineSimilarity;

use strict;



#
# Load simple list of data -- top GEO6's:
#
my %H = ();
#
open( FIN, "cat flist_top_geo6 |" );
while( my $ln = <FIN> ){
    chomp( $ln );
    $H{$ln} = 1;
}
close( FIN );



#
#   Start creating DL input file
#
my $cnt = 0;
#
open( FIN, "gzip -cd training.csv.gz |" );
open( FOUT1, "> training_for_CNN_01.csv" );
#
while( my $ln = <FIN> ){
    chomp( $ln );

    if( $cnt == 0 ){   $cnt ++;   next;   }     # SKIP Header of file
    
    # qp03pn,10,14:30,0.024720973824962248
    my( $geo6, $dd, $hh, $demand ) = split( /\,/, $ln );

    # load selected ones only...
    if( ! defined( $H{$geo6} )){   next;   }
    
    my( $hhh, $mmm ) = split( /\:/, $hh);
    # my $abstime = ($dd -1) * 24 * 4 + $hhh * 4 + ($mmm / 15);
    
    if( $demand =~ /^([0-9])\.([0-9]+)e\-([0-9]+)/ ){
 	my( $first, $sec, $exp ) = ($1, $2, $3 );
 	$demand = "0.";
 	for( my $i = 1; $i < $exp; $i ++ ){    $demand .= "0";   }
 	$demand .= "$first$sec";
    }

    my $ndd = $dd / 61;
    $ndd =~ s/^(0\......).*$/$1/;
    my $nhhh = $hhh / 23;
    $nhhh =~ s/^(0\......).*$/$1/;
    my $nmmm = $mmm / 45;
    $nmmm =~ s/^(0\......).*$/$1/;
    #  DEMAND is ALREADY normalized...
    #
    print FOUT1 "$geo6 $ndd $nhhh $nmmm $demand\n";
}
#
close( FOUT1 );
close( FIN );

