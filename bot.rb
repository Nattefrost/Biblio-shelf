#!/usr/local/bin/ruby
require 'sqlite3'
require 'socket'

# Don't allow use of "tainted" data by potentially dangerous operations

$SAFE=1

# The irc class, which talks to the server and holds the main event loop

class IRC

    def initialize
        @server = 'irc.freenode.net'

        @port = 6667

        @nick = 'BooksBot'

        @channel = '#nattebooks'

        @COMMANDS = ['??author','??title','??publisher']
    end

    def send(s)

        # Send a message to the irc server and print it to the screen

        puts "--> #{s}"

        @irc.send "#{s} \r\n", 0 
    end

    def connect()

        # Connect to the IRC server

        @irc = TCPSocket.open(@server, @port)
        send 'USER nattefrost_books x x :blah blah'
        send "NICK #{@nick}"
        send "JOIN #{@channel}"
    end

    def read_db
      db = SQLite3::Database.open '/home/nattefrost/dev/NatteBiblio/books.db'
      res = db.execute 'SELECT title, author, editor, read
                   FROM Books B
                   JOIN Authors A
                   ON B.author_id = A.id
                   JOIN Editors E
                   ON B.editor_id = E.id;'
      return res
    end

    def get_author_books(author)
      db = SQLite3::Database.open './books.db'
      books = db.execute "SELECT title, author, editor
                        FROM Books B
                        Join Authors A
                        ON B.Author_id = A.id
                        JOIN Editors E
                        ON B.editor_id = E.id
                        WHERE author = '#{author}' COLLATE NOCASE"
      return books
    end

    def evaluate(s)

        # Make sure we have a valid expression (for security reasons), and

        # evaluate it if we do, otherwise return an error message

        if s =~ /^[-+*\/\d\s\eE.()]*$/ then

            begin

                s.untaint

                return eval(s).to_s

            rescue Exception => detail

                puts detail.message()
            end
        end

        return 'Error'
    end

    def handle_server_input(s)
      # Looking for known commands and fetching data accordingly.
        s = s.downcase()
        idx = s.index('??')
        if idx then
          data = s[idx..s.length]
          data = data.split(' ')
          cmd1, arg1 = data[0].split('=')[0], data[0].split('=')[1] #good
          puts cmd1
          puts arg1
          if cmd1 == '??author' then
            books = get_author_books(arg1)
            puts books
            send "PRIVMSG #{@channel} : #{books} "
          end

        end

    end



    def main_loop
        while true
            ready = select([@irc, $stdin], nil, nil, nil)

            next if not ready

            for s in ready[0]

                if s == $stdin then

                    return if $stdin.eof

                    s = $stdin.gets

                    send s

                elsif s == @irc then

                    return if @irc.eof

                    s = @irc.gets

                    handle_server_input(s)

                end
            end
        end
    end
end
# The main program

# If we get an exception, then print it out and keep going (we do NOT want

# to disconnect unexpectedly!)

irc = IRC.new()
irc.connect()

begin

    irc.main_loop()

rescue Interrupt

rescue Exception => detail

    puts detail.message()

    print detail.backtrace.join("\n")

    retry

end
