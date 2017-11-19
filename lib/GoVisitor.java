
public class GoVisitor extends PlSqlParserBaseVisitor<StringBuilder> {

    @Override
    public StringBuilder visitSql_script(PlSqlParser.Sql_scriptContext ctx) {
        return new StringBuilder("uyy");
    }

}