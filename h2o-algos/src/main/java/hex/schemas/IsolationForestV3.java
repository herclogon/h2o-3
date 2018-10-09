package hex.schemas;

import hex.tree.isofor.IsolationForest;
import hex.tree.isofor.IsolationForestModel;
import water.api.API;

public class IsolationForestV3 extends SharedTreeV3<IsolationForest, IsolationForestV3, IsolationForestV3.IsolationForestParametersV3> {

    public static final class IsolationForestParametersV3 extends SharedTreeV3.SharedTreeParametersV3<IsolationForestModel.IsolationForestParameters, IsolationForestParametersV3> {
        static public String[] fields = new String[]{
                "model_id",
                "training_frame",
                "score_each_iteration",
                "score_tree_interval",
                "ignored_columns",
                "ignore_const_cols",
                "ntrees",
                "max_depth",
                "min_rows",
                "nbins",
                "nbins_top_level",
                "nbins_cats",
                "max_runtime_secs",
                "seed",
                "build_tree_one_node",
                "mtries",
                "checkpoint",
                "col_sample_rate_change_per_level",
                "col_sample_rate_per_tree",
                "categorical_encoding"
        };

        // Input fields
        @API(help = "Number of variables randomly sampled as candidates at each split. If set to -1, defaults p/3 for regression (where p is the # of predictors)", gridable = true)
        public int mtries;
    }
}
