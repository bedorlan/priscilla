import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class S2S {
    public static void main(String[] args) throws Exception {

        if (args.length != 1) {
            System.err.println("pkg missing");
            return;
        }

        final String[] pkgs = args;

        for(String file : pkgs) {
            ANTLRFileStream input = new ANTLRFileStream(file);
            PlSqlLexer lexer = new PlSqlLexer(input);
            CommonTokenStream tokens = new CommonTokenStream(lexer);
            PlSqlParser parser = new PlSqlParser(tokens);
            ParseTree tree = parser.sql_script();
            GoVisitor visitor = new GoVisitor();

            String output = visitor.visit(tree).toString();
            System.out.println(output);
        }
    }
}
