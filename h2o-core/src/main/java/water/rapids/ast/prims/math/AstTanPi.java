package water.rapids.ast.prims.math;

@Deprecated
public class AstTanPi extends AstUniOp {
  @Override
  public String str() {
    return "tanpi";
  }

  @Override
  public double op(double d) {
    return Math.tan(Math.PI * d);
  }
}
