#!/usr/bin/perl
use warnings;

my $width = $ARGV[0];
my $height = $ARGV[1];

# block sizes
my $size1 = 3;
my $size2 = 4.5;

# will be used to keep track of all the possible next lines
# for each possible current line
my %poss_seqs = ();

my $count = 0;
# only run this stuff if neither width nor height are 0
if ($width && $height) {
    my %poss_widths1 = gen_possible_widths($size1);
    my %poss_widths2 = gen_possible_widths($size2);
    
    my %block_combos = ();
    foreach my $n_size1 (keys %poss_widths1) {
        my $n_size2 = calc_remaining($n_size1);
        next if (not defined $poss_widths2{$n_size2});
        
        my @size1_seq = map { $size1 } (1..$n_size1);
        my @size2_seq = map { $size2 } (1..$n_size2);
        
        my @perms = perm([], (@size1_seq, @size2_seq));
        foreach (@perms) {
            my $tabbed = join("\t", @$_);
            $block_combos{$tabbed} = 1;
        }      
    }
    
    my @combos = keys %block_combos;
    
    foreach my $perm (@combos) {
        foreach (@combos) {
            next if ($_ eq $perm || has_common_cracks($perm, $_));
            push @{$poss_seqs{$perm}}, $_;
        }
    }
    
    print count_poss_next(\@combos, $height)+1, "\n";
} else {
    print $count, "\n";
}

##############
## SUBROUTINES
##############

# recursively counts the number of possible next line of blocks
sub count_poss_next {
    my ($combos, $lines_rem) = @_;
    my @candidates = @$combos;
    
    if ($lines_rem) {
        $lines_rem--;
        $count += $#candidates;
        foreach my $combo (@candidates) {
            count_poss_next($poss_seqs{$combo}, $lines_rem);
        }
    }
    
    return $count;
}

# checks if the given 2 lines of blocks have any cracks that line up
sub has_common_cracks {
    my ($curr, $next) = @_;
    my @c_cracks = find_cracks($curr);
    my @n_cracks = find_cracks($next);
    
    my %all_cracks = ();
    foreach (sort (@c_cracks, @n_cracks)) {
        next if ($_ == $width);     # ignore the crack locations that indicate end of line
        if (defined $all_cracks{$_}) {
            return 1;
        } else {
            $all_cracks{$_} = 1;
        }
    }
    
    return 0;
}

# find all the locations of block cracks
sub find_cracks {
    my ($line) = @_;
    my $value = 0;
    return map { $value += $_ } split("\t", $line);
}

# generates the permutations of a list of blocks
sub perm {
    my ($result, @avail) = @_;
    return $result if !@avail;

    my @list;
    for my $i (0..$#avail) {
        my $e = splice @avail, $i, 1;
        push @list, perm([@$result, $e], @avail);
        splice @avail, $i, 0, $e;
    }
    return @list;
}

# uses the slope-intercept form to calculate how many size2 blocks are needed
# when we're using some x number of size1 blocks
sub calc_remaining {
    my ($x) = @_;
    return ($width - $size1*$x)/$size2;
}

# returns all the possible widths that can be constructed
# given the size of the block
sub gen_possible_widths {
    my ($size) = @_;
    
    my %poss_widths = ();
    my $i = 0;
    my $curr_width = 0;
    while ( ($curr_width < $width) && (($curr_width+$size) <= $width) ) {
        $curr_width = $i * $size;
        $poss_widths{$i} = $curr_width;
        $i++;
    }
    
    return %poss_widths;
}