#!/usr/bin/perl

use strict;
use DBI;
use CGI;




sub get_data()
{
    my $dbh = DBI->connect(          
        "dbi:SQLite:dbname=books.db", 
        "",                          
        "",                       
        { RaiseError => 1 },         
    ) or die $DBI::errstr;


    
    my $sth = $dbh->prepare("SELECT id, title, author, editor, read
             FROM Books B
             JOIN Authors A
             ON B.author_id = A.id
             JOIN Editors E
             ON B.editor_id = E.id; ");
    $sth->execute();


# Printing in a loop
    print "<div align='center'> ";
    print "<table CELLPADDING=2><TR><TH>ID</TH><TH>Titre</TH><TH>Auteur</TH><TH>Editeur</TH><TH>Lu ?</TH></TR>";
    my $row;
    my $i = 1;
    while ($row = $sth->fetchrow_arrayref())
    {
        my $read;
        if (@$row[4] == 1) {
            $read = "Oui";
        } else {
            $read = "Non";
        }
        
        print " <TR><TD> @$row[0]</TD><TD> @$row[1]</TD><TD> @$row[2]</TD><TD> @$row[3]</TD><TD> $read</TD></TR>";
        $i += 1;
    }


    $sth->finish();
    $dbh->disconnect();
    print "</table> </div>";
}


# Actually displaying as html
my $cgi = CGI->new;
print $cgi->header(-type => 'text/html',
                   -charset => 'utf-8');
print $cgi->start_html(-title => "Livres",
                       -bgcolor => "black",
                       -text => "white",
                       -charset=>"UTF-8",
                       -encoding=>"UTF-8");

print  "<style type='text/css'>

        body {
            font-family: verdana ;
            font-size: 100% ;
            text-align: center ;
            }

        table {
            border-collapse: collapse;
        }

        table, th, td {
            border: 1px solid dodgerblue;
        }

        </style>";

&get_data();

print $cgi-> end_html;